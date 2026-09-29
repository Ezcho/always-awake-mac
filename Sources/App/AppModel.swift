import AppKit
import ServiceManagement

@MainActor
final class AppModel {
    var active = false { didSet { updateMaintenance(); onChange?() } }
    var busy = false { didSet { onChange?() } }
    var monitorOn = UserDefaults.standard.object(forKey: "monitorOn") as? Bool ?? true { didSet { onChange?() } }
    var error: String? { didSet { onChange?() } }
    var recoveryRequired = false { didSet { updateMaintenance(); onChange?() } }
    var serviceReady = false { didSet { onChange?() } }
    var needsApproval = false { didSet { onChange?() } }
    let display = DisplayController()
    let client = HelperClient()
    private let service = SMAppService.daemon(plistName: AppIdentity.helperPlist)
    private var timer: Timer?
    private var heartbeatInFlight = false
    private var activity: NSObjectProtocol?
    var onChange: (() -> Void)?

    init() {
        refreshService()
        display.onError = { [weak self] message in self?.error = message }
        client.onDisconnect = { [weak self] in
            guard let self else { return }
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
                if self.active { self.sendHeartbeat() }
                self.refreshService()
            }
        }
    }

    func refreshService() {
        serviceReady = service.status == .enabled
        needsApproval = service.status == .requiresApproval
    }

    func prepareService() {
        // A stable installation path is required by ServiceManagement and app updates.
        guard Bundle.main.bundleURL.deletingLastPathComponent().path == "/Applications" else {
            error = "Always Awake.app을 응용 프로그램 폴더로 옮긴 다음 다시 실행해 주세요."
            NSWorkspace.shared.selectFile(Bundle.main.bundleURL.path, inFileViewerRootedAtPath: "")
            return
        }
        do {
            if service.status == .notRegistered || service.status == .notFound { try service.register() }
            refreshService()
            if needsApproval { SMAppService.openSystemSettingsLoginItems() }
            error = serviceReady ? nil : "시스템 설정 → 로그인 항목 및 확장 프로그램에서 Always Awake를 허용해 주세요."
        } catch {
            // register() may throw authorization-required after successfully recording
            // the daemon. Treat that as onboarding, not a failed installation.
            refreshService()
            if needsApproval {
                self.error = "최초 한 번 macOS 승인이 필요합니다. 로그인 항목에서 Always Awake를 허용해 주세요."
                SMAppService.openSystemSettingsLoginItems()
            } else { self.error = "보조 서비스를 준비하지 못했습니다. \(error.localizedDescription)" }
        }
    }

    func toggleSession(completion: (() -> Void)? = nil) {
        guard !busy else { completion?(); return }
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
                self.active = true
                self.activity = ProcessInfo.processInfo.beginActivity(options: [.userInitiated, .idleSystemSleepDisabled], reason: "Always Awake session heartbeat")
                do { try self.display.apply(keepOn: self.monitorOn) }
                catch { self.error = error.localizedDescription }
            case .failure(let failure): self.error = failure.localizedDescription; self.refreshService()
            }
            self.onChange?()
        }
    }

    func stop(completion: ((Bool) -> Void)? = nil) {
        busy = true
        display.release()
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
        monitorOn = value
        UserDefaults.standard.set(value, forKey: "monitorOn")
        if active {
            do { try display.apply(keepOn: value) }
            catch { self.error = error.localizedDescription }
        }
    }

    func removeService() {
        guard !busy else { return }
        let remove: () -> Void = {
            Task { @MainActor in
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

    private func localStop() {
        active = false
        display.release()
        if let activity { ProcessInfo.processInfo.endActivity(activity); self.activity = nil }
    }
}
