import AppKit

@MainActor
final class AppUpdateController: NSObject {
    private let model: AppModel
    private let handoff: () -> Void
    var onChange: (() -> Void)?
    private(set) var available: UpdateRelease?
    private var working = false
    private var status = "최신 버전을 확인합니다."
    private var window: NSWindow?
    private let label = NSTextField(wrappingLabelWithString: "")
    private let button = NSButton(title: "업데이트 확인", target: nil, action: nil)
    private let progress = NSProgressIndicator()
    private let downloadLink = NSButton(title: "다운로드 페이지", target: nil, action: nil)
    private var installerPackage: URL?
    private var nextAutomaticCheck = Date.distantPast

    var menuTitle: String { available.map { "pika \($0.version) 업데이트…" } ?? "업데이트 확인…" }

    init(model: AppModel, handoff: @escaping () -> Void) {
        self.model = model
        self.handoff = handoff
    }

    func checkAutomatically() {
        let last = UserDefaults.standard.double(forKey: "lastUpdateCheck")
        guard !working, Date() >= nextAutomaticCheck, Date().timeIntervalSince1970 - last > 86_400 else { return }
        // Activation after a failed check must not repeatedly consume the fallback API quota.
        nextAutomaticCheck = Date().addingTimeInterval(900)
        check()
    }

    func present() {
        if window == nil {
            let window = NSWindow(contentRect: NSRect(x: 0, y: 0, width: 360, height: 192),
                                  styleMask: [.titled, .closable], backing: .buffered, defer: false)
            window.title = "pika 업데이트 · \(AppIdentity.version)"
            window.isReleasedWhenClosed = false
            window.center()
            label.frame = NSRect(x: 24, y: 73, width: 312, height: 94)
            label.font = .systemFont(ofSize: 13)
            button.frame = NSRect(x: 152, y: 22, width: 184, height: 32)
            button.bezelStyle = .rounded
            button.target = self
            button.action = #selector(action)
            progress.frame = NSRect(x: 24, y: 29, width: 20, height: 20)
            progress.style = .spinning
            progress.isDisplayedWhenStopped = false
            downloadLink.frame = NSRect(x: 22, y: 22, width: 122, height: 32)
            downloadLink.bezelStyle = .rounded
            downloadLink.target = self
            downloadLink.action = #selector(openDownloadPage)
            for view in [label, button, progress, downloadLink] { window.contentView?.addSubview(view) }
            self.window = window
        }
        render()
        NSApp.activate(ignoringOtherApps: true)
        window?.makeKeyAndOrderFront(nil)
        if !working && available == nil { check() }
    }

    private func render() {
        label.stringValue = status
        button.title = available == nil ? "다시 확인" : "업데이트 설치…"
        button.isEnabled = !working
        downloadLink.isHidden = working
        downloadLink.title = installerPackage == nil ? "다운로드 페이지" : "설치 파일 보기"
        if working { progress.startAnimation(nil) } else { progress.stopAnimation(nil) }
        onChange?()
    }

    @objc private func action() {
        if available != nil { beginUpdate() } else { check() }
    }

    @objc private func openDownloadPage() {
        if let installerPackage { NSWorkspace.shared.activateFileViewerSelecting([installerPackage]) }
        else { NSWorkspace.shared.open(URL(string: "https://no-sleep-pika.online/")!) }
    }

    private func check() {
        guard !working else { return }
        working = true
        status = "최신 버전을 확인하는 중…"
        render()
        Task { @MainActor in
            defer { self.working = false; self.render() }
            do {
                let release = try await UpdateDownload.release()
                UserDefaults.standard.set(Date().timeIntervalSince1970, forKey: "lastUpdateCheck")
                available = release.isNewer(than: AppIdentity.version) ? release : nil
                status = available == nil ? "최신 버전입니다.\npika \(AppIdentity.version)" :
                    "pika \(release.version)을 사용할 수 있습니다.\n\n앱에서 설치 파일을 받아 macOS 설치 프로그램을 엽니다. 설치 완료 후 pika를 다시 여세요."
            } catch { status = error.localizedDescription }
        }
    }

    private func beginUpdate() {
        guard !working, let release = available else { return }
        guard !model.busy else { status = "진행 중인 작업이 끝난 뒤 다시 시도해 주세요."; render(); return }
        guard Bundle.main.bundleURL.standardizedFileURL.path == "/Applications/pika.app" else {
            status = "이번에는 홈페이지의 PKG를 설치해 주세요. 앱 내 업데이트는 /Applications/pika.app에서 지원합니다."
            render(); return
        }
        let alert = NSAlert()
        alert.messageText = "pika \(release.version)으로 업데이트할까요?"
        alert.informativeText = "Session을 종료하고 검증한 PKG를 macOS 설치 프로그램으로 엽니다. 설치 프로그램이 열리면 pika는 종료됩니다. 관리자 승인을 거쳐 설치한 후 응용 프로그램에서 pika를 다시 여세요. 덮개를 열고 진행해 주세요."
        alert.addButton(withTitle: "업데이트")
        alert.addButton(withTitle: "취소")
        guard alert.runModal() == .alertFirstButtonReturn else { return }
        guard !model.busy else { return }
        working = true
        status = "Session을 종료하고 잠자기 설정을 복구하는 중…"
        render()
        if model.active || model.recoveryRequired {
            model.stop { [weak self] success in
                guard let self else { return }
                if success { self.download(release) }
                else { self.fail(self.model.error ?? "잠자기 설정을 복구하지 못해 업데이트를 중단했습니다.") }
            }
        } else { download(release) }
    }

    private func fail(_ message: String) {
        model.busy = false
        working = false
        status = message
        render()
    }

    private func download(_ release: UpdateRelease) {
        // Session is already stopped. Busy blocks menu and MCP mutations until handoff.
        guard !model.active, !model.recoveryRequired, !model.busy else {
            fail("Session이 종료되지 않아 업데이트를 중단했습니다."); return
        }
        model.busy = true
        status = "pika \(release.version) 다운로드·검증 중…"
        render()
        Task { @MainActor in
            do {
                try SystemSleepController.requireSystemSleepEnabled()
                let package: URL
                if let retained = installerPackage, retained.lastPathComponent == "pika-\(release.version).pkg" {
                    try release.verify(retained)
                    package = retained
                } else {
                    let temporary = try await UpdateDownload.package(release)
                    defer { try? FileManager.default.removeItem(at: temporary.deletingLastPathComponent()) }
                    package = try UpdatePackageStore.retain(temporary, release: release)
                    installerPackage = package
                }
                try await model.prepareForUpdate()
                guard !model.active, !model.recoveryRequired else { throw AwakeError("Session 복구가 필요해 업데이트를 중단했습니다.") }
                try SystemSleepController.requireSystemSleepEnabled()
                status = "macOS 설치 프로그램을 여는 중…"
                render()
                try await SystemInstallerHandoff.open(package, release: release)
                // Opening Installer is not installation success. The PKG stays at a
                // stable path so Gatekeeper approval or a later retry can reopen it.
                handoff()
            } catch {
                fail(error.localizedDescription)
            }
        }
    }
}
