import AppKit
import ServiceManagement

@MainActor
final class AppModel {
    var active = false { didSet { updateMaintenance(); onChange?() } }
    var busy = false { didSet { onChange?() } }
    private var monitorPreference = UserDefaults.standard.object(forKey: "monitorOn") as? Bool ?? true
    var monitorOn: Bool { active && monitorPreference }
    var error: String? { didSet { onChange?() } }
    var recoveryRequired = false { didSet { updateMaintenance(); onChange?() } }
    var serviceReady = false { didSet { onChange?() } }
    var needsApproval = false { didSet { onChange?() } }
    var helperConnected = false { didSet { onChange?() } }
    var setupStatus: String? { didSet { onChange?() } }
    var onSetupRequested: (() -> Void)?
    private let requiresInstalledHelper = Signature.isAdHoc(Bundle.main.bundleURL.appendingPathComponent("Contents/Library/HelperTools/AlwaysAwakeHelper"))
    private(set) var installedHelperReady = false
    // Retained in the MCP status schema for older clients. Sessions require lid support.
    var standardModeAvailable: Bool { false }
    private(set) var sessionMode = "off"
    private(set) var lidEngaged = false
    var waitingForLid: Bool { active && sessionMode == "closedLid" && !lidEngaged }
    var lidClosedSupported: Bool { active && sessionMode == "closedLid" }
    var sessionNotice: String? {
        if waitingForLid { return "대기 중 · 덮개를 닫으면 시작" }
        if active && lidEngaged { return "덮개 닫힘 · 실행 중" }
        if installedHelperReady { return active ? "덮개 잠자기 방지 활성" : "덮개 모드 · 보조 서비스 설치됨" }
        if InstalledHelper.isPresent { return "보조 서비스 재설치 필요" }
        if requiresInstalledHelper { return "덮개 모드 · 보조 서비스 설치 필요" }
        return active ? "덮개 잠자기 방지 활성" : nil
    }
    let display = DisplayController()
    let client = HelperClient()
    private let service = SMAppService.daemon(plistName: AppIdentity.helperPlist)
    private var timer: Timer?
    private var lidTimer: Timer?
    private var heartbeatInFlight = false
    private var checkingHelper = false
    private var activity: NSObjectProtocol?
    var onChange: (() -> Void)?

    init() {
        refreshService()
        display.onError = { [weak self] message in self?.error = message }
        client.onDisconnect = { [weak self] in
            guard let self else { return }
            self.helperConnected = false
            self.setupStatus = nil
            let wasActive = self.active
            self.localStop()
            self.refreshService()
            if wasActive {
                self.recoveryRequired = true
                self.error = "연결이 끊겨 세션을 중단했습니다. 보조 서비스가 잠자기 설정을 복구합니다."
            }
            self.onChange?()
        }
        NSWorkspace.shared.notificationCenter.addObserver(forName: NSWorkspace.didWakeNotification, object: nil, queue: .main) { [weak self] _ in
            Task { @MainActor in
                guard let self else { return }
                if self.active { self.tick() }
                self.refreshService()
            }
        }
    }

    func refreshService() {
        if InstalledHelper.isPresent {
            installedHelperReady = (try? InstalledHelper.validateForClient()) != nil
            serviceReady = installedHelperReady
            needsApproval = false
            return
        }
        installedHelperReady = false
        // The ad-hoc app-managed daemon can be registered yet rejected by
        // launchd. Use the separate, user-authorized helper installer instead.
        if requiresInstalledHelper {
            serviceReady = false
            needsApproval = false
            return
        }
        serviceReady = service.status == .enabled
        needsApproval = service.status == .requiresApproval
    }

    func prepareService() {
        setupStatus = nil
        if InstalledHelper.isPresent {
            do { try InstalledHelper.validateForClient() }
            catch { self.error = error.localizedDescription; onSetupRequested?() }
            return
        }
        guard !requiresInstalledHelper else {
            error = "덮개 모드에는 보조 서비스가 필요합니다. 설치 안내에서 pika PKG를 다시 설치해 주세요."
            onSetupRequested?()
            return
        }
        // A stable installation path is required by ServiceManagement and app updates.
        guard Bundle.main.bundleURL.deletingLastPathComponent().path == "/Applications" else {
            error = "pika.app을 응용 프로그램 폴더로 옮긴 다음 다시 실행해 주세요."
            NSWorkspace.shared.selectFile(Bundle.main.bundleURL.path, inFileViewerRootedAtPath: "")
            return
        }
        do {
            if service.status == .notRegistered || service.status == .notFound { try service.register() }
            refreshService()
            if needsApproval { SMAppService.openSystemSettingsLoginItems() }
            error = serviceReady ? nil : "시스템 설정 → 로그인 항목 및 확장 프로그램에서 pika를 허용해 주세요."
        } catch {
            // register() may throw authorization-required after successfully recording
            // the daemon. Treat that as onboarding, not a failed installation.
            refreshService()
            if needsApproval {
                self.error = "최초 한 번 macOS 승인이 필요합니다. 로그인 항목에서 pika를 허용해 주세요."
                SMAppService.openSystemSettingsLoginItems()
            } else { self.error = "보조 서비스를 준비하지 못했습니다. \(error.localizedDescription)" }
        }
    }

    func toggleSession(completion: (() -> Void)? = nil) {
        guard !busy else { completion?(); return }
        setupStatus = nil
        refreshService()
        if active || recoveryRequired { stop { _ in completion?() }; return }
        guard serviceReady else { prepareService(); completion?(); return }
        if let issue = HardwareReading.current().issue { error = issue; completion?(); return }
        busy = true
        error = nil
        client.call(.start) { [weak self] result in
            defer { completion?() }
            guard let self else { return }
            self.busy = false
            switch result {
            case .success(let reply):
                self.recoveryRequired = reply.recoveryRequired
                guard reply.active && reply.ownedByCaller else {
                    self.error = reply.message ?? "세션을 시작하지 못했습니다."
                    self.onChange?()
                    return
                }
                self.sessionMode = "closedLid"
                self.helperConnected = true
                self.active = true
                self.activity = ProcessInfo.processInfo.beginActivity(options: [.userInitiated, .idleSystemSleepDisabled], reason: "pika session heartbeat")
                self.startLidObservation()
            case .failure(let failure):
                self.error = failure.localizedDescription
                self.helperConnected = false
                self.refreshService()
                self.onSetupRequested?()
            }
            self.onChange?()
        }
    }

    func stop(completion: ((Bool) -> Void)? = nil) {
        busy = true
        setupStatus = nil
        stopLidObservation()
        display.disarm()
        client.call(.stop) { [weak self] result in
            guard let self else { return }
            self.busy = false
            switch result {
            case .success(let reply):
                self.recoveryRequired = reply.recoveryRequired
                if !reply.active { self.localStop() }
                if !reply.active && !reply.recoveryRequired {
                    self.error = reply.message
                    completion?(true)
                } else {
                    if self.active && reply.ownedByCaller { self.startLidObservation() }
                    self.error = reply.message ?? "잠자기 설정 복구가 필요합니다. 다시 OFF를 눌러 주세요."
                    completion?(false)
                }
            case .failure(let failure):
                self.localStop()
                self.recoveryRequired = true
                self.error = failure.localizedDescription
                completion?(false)
            }
            self.onChange?()
        }
    }

    func setMonitor(_ value: Bool) {
        guard active, !busy else { return }
        do {
            // While armed, Monitor only selects what to do after the lid closes.
            if lidEngaged {
                try display.apply(keepOn: value)
            }
            monitorPreference = value
            UserDefaults.standard.set(value, forKey: "monitorOn")
        }
        catch { self.error = error.localizedDescription }
        onChange?()
    }

    func checkHelperConnection() {
        guard !busy, !active, !checkingHelper else { return }
        refreshService()
        guard serviceReady else { helperConnected = false; setupStatus = nil; return }
        checkingHelper = true
        client.call(.status) { [weak self] result in
            guard let self else { return }
            self.checkingHelper = false
            guard !self.busy, !self.active else { return }
            switch result {
            case .success(let reply):
                self.helperConnected = true
                self.recoveryRequired = reply.recoveryRequired
                self.setupStatus = reply.recoveryRequired ? "잠자기 설정 복구가 필요합니다. 제어창에서 Session OFF를 눌러 주세요." : "보조 서비스 연결 완료"
            case .failure(let failure):
                self.helperConnected = false
                self.setupStatus = failure.localizedDescription
            }
        }
    }

    func installHelper() {
        guard !busy else { return }
        guard !active, !recoveryRequired else {
            setupStatus = "먼저 제어창에서 Session을 OFF로 바꾸고 복구가 끝난 뒤 설치해 주세요."
            return
        }
        guard Bundle.main.bundleURL.standardizedFileURL.path == "/Applications/pika.app" else {
            setupStatus = "홈페이지의 pika PKG를 설치한 뒤 응용 프로그램에서 다시 실행해 주세요."
            return
        }
        busy = true
        setupStatus = "pika 통합 설치 파일을 다운로드하고 확인하는 중…"
        Task { @MainActor in
            defer { self.busy = false }
            do {
                try SystemSleepController.requireSystemSleepEnabled()
                let package = try await HelperSetupDownload.download()
                // Never replace an active lease or relax macOS security settings.
                guard !self.active, !self.recoveryRequired else { throw AwakeError("Session을 먼저 OFF로 바꿔 주세요.") }
                try SystemSleepController.requireSystemSleepEnabled()
                self.client.invalidate()
                if self.service.status != .notRegistered && self.service.status != .notFound {
                    self.setupStatus = "이전 보조 서비스 등록을 정리하는 중…"
                    try await self.service.unregister()
                    try await Task.sleep(nanoseconds: 2_000_000_000)
                    guard self.service.status == .notRegistered || self.service.status == .notFound else {
                        throw AwakeError("이전 보조 서비스 등록 해제가 아직 완료되지 않았습니다. 잠시 뒤 다시 시도해 주세요.")
                    }
                }
                try SystemSleepController.requireSystemSleepEnabled()
                // Reveal the verified PKG; never race Installer against app shutdown.
                // The user quits explicitly, and the distribution asks to close pika.
                NSWorkspace.shared.activateFileViewerSelecting([package])
                self.setupStatus = "PKG 다운로드 완료. 아래 ‘pika 종료’를 누른 뒤 Finder에 선택된 설치 파일을 여세요."
            } catch {
                self.setupStatus = error.localizedDescription
                self.error = error.localizedDescription
                self.refreshService()
            }
        }
    }

    func prepareForUpdate() async throws {
        guard busy, !active, !recoveryRequired else { throw AwakeError("먼저 Session 복구를 완료해 주세요.") }
        try SystemSleepController.requireSystemSleepEnabled()
        client.invalidate()
        if service.status != .notRegistered && service.status != .notFound {
            try await service.unregister()
            try await Task.sleep(nanoseconds: 2_000_000_000)
            guard service.status == .notRegistered || service.status == .notFound else {
                throw AwakeError("이전 보조 서비스가 종료되는 중입니다. 잠시 뒤 다시 시도해 주세요.")
            }
        }
        try SystemSleepController.requireSystemSleepEnabled()
    }

    func removeService() {
        guard !busy else { return }
        if InstalledHelper.isPresent {
            error = "설치된 보조 서비스는 Session을 OFF로 바꾼 뒤 pika 제거 패키지로 삭제해 주세요."
            return
        }
        let remove: () -> Void = {
            self.busy = true
            Task { @MainActor in
                defer { self.busy = false; self.refreshService() }
                do {
                    self.client.invalidate()
                    try await self.service.unregister()
                    self.refreshService()
                    self.error = "보조 서비스를 제거했습니다. 종료 후 앱을 휴지통으로 옮기면 됩니다."
                } catch { self.error = "보조 서비스 제거 실패: \(error.localizedDescription)" }
            }
        }
        if active || recoveryRequired { stop { if $0 { remove() } } } else { remove() }
    }

    // No UI clock or hardware polling while idle. Keep the lease alive even while
    // a native menu is tracking, which runs outside the default run-loop mode.
    private func updateMaintenance() {
        guard active || recoveryRequired else {
            timer?.invalidate()
            timer = nil
            return
        }
        guard timer == nil else { return }
        let value = Timer(timeInterval: 10, repeats: true) { [weak self] _ in
            Task { @MainActor in self?.tick() }
        }
        value.tolerance = 1
        RunLoop.main.add(value, forMode: .common)
        timer = value
    }

    private func tick() {
        if active && !busy { sendHeartbeat() }
        if recoveryRequired { refreshService() }
        if recoveryRequired && !active && !busy && serviceReady {
            client.call(.status) { [weak self] result in
                guard let self, case .success(let reply) = result else { return }
                if reply.active && reply.ownedByCaller { self.stop(); return }
                self.recoveryRequired = reply.recoveryRequired || reply.active
                if !reply.active && !reply.recoveryRequired {
                    self.error = "잠자기 설정을 복구했습니다. 세션을 다시 시작할 수 있습니다."
                }
            }
        }
    }

    private func sendHeartbeat() {
        guard sessionMode == "closedLid" else { return }
        guard !heartbeatInFlight else { return }
        heartbeatInFlight = true
        client.call(.heartbeat) { [weak self] result in
            guard let self else { return }
            self.heartbeatInFlight = false
            switch result {
            case .success(let reply):
                if !reply.active || !reply.ownedByCaller {
                    self.localStop()
                    self.error = reply.message ?? "세션이 종료되었습니다."
                }
                self.recoveryRequired = reply.recoveryRequired
            case .failure(let failure):
                self.localStop()
                self.recoveryRequired = true
                self.error = failure.localizedDescription
            }
            self.onChange?()
        }
    }

    private func startLidObservation() {
        stopLidObservation()
        display.arm()
        updateLidState()
        // Read only the lid registry value here; full safety checks and the helper
        // lease retain their existing cadence. Never poll when Session is OFF.
        let value = Timer(timeInterval: 1, repeats: true) { [weak self] _ in
            Task { @MainActor in self?.updateLidState() }
        }
        value.tolerance = 0.2
        RunLoop.main.add(value, forMode: .common)
        lidTimer = value
    }

    private func stopLidObservation() {
        lidTimer?.invalidate()
        lidTimer = nil
        lidEngaged = false
    }

    private func updateLidState() {
        guard active, !busy, sessionMode == "closedLid" else { return }
        // Unknown lid state must not trigger a display sleep request.
        guard let closed = HardwareReading.lidIsClosed(), closed != lidEngaged else { return }
        lidEngaged = closed
        if closed {
            do { try display.apply(keepOn: monitorOn) }
            catch { self.error = error.localizedDescription }
        } else {
            // Reopening cancels any delayed sleep and returns to the armed state.
            display.release()
        }
        onChange?()
    }

    private func localStop() {
        stopLidObservation()
        sessionMode = "off"
        active = false
        display.disarm()
        if let activity { ProcessInfo.processInfo.endActivity(activity); self.activity = nil }
    }

}
