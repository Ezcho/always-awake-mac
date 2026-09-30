import AppKit
import Darwin

@MainActor
final class UpdateDelegate: NSObject, NSApplicationDelegate, NSWindowDelegate {
    let package: URL
    let release: UpdateRelease
    let parent: pid_t
    let directory: URL
    private var window: NSWindow!
    private let label = NSTextField(wrappingLabelWithString: "pika 종료를 기다리는 중…")
    private let progress = NSProgressIndicator()
    private let retry = NSButton(title: "다시 시도", target: nil, action: nil)
    private let reopen = NSButton(title: "pika 열기", target: nil, action: nil)
    private var installing = false
    private var waitTimer: Timer?
    private let deadline = Date().addingTimeInterval(45)

    init(package: URL, release: UpdateRelease, parent: pid_t) {
        self.package = package; self.release = release; self.parent = parent
        self.directory = package.deletingLastPathComponent()
    }
    func applicationDidFinishLaunching(_ notification: Notification) {
        NSApp.setActivationPolicy(.regular)
        window = NSWindow(contentRect: NSRect(x: 0, y: 0, width: 380, height: 190), styleMask: [.titled, .closable], backing: .buffered, defer: false)
        window.title = "pika \(release.version) 업데이트"
        window.delegate = self
        window.isReleasedWhenClosed = false
        window.center()
        label.frame = NSRect(x: 24, y: 65, width: 332, height: 100)
        label.font = .systemFont(ofSize: 13)
        progress.style = .spinning
        progress.isDisplayedWhenStopped = false
        progress.frame = NSRect(x: 24, y: 25, width: 20, height: 20)
        for (button, x, action) in [(retry, 122.0, #selector(install)), (reopen, 244.0, #selector(openApp))] {
            button.frame = NSRect(x: x, y: 18, width: 112, height: 32)
            button.bezelStyle = .rounded
            button.target = self
            button.action = action
            button.isHidden = true
        }
        for view in [label, progress, retry, reopen] { window.contentView?.addSubview(view) }
        window.makeKeyAndOrderFront(nil)
        NSApp.activate(ignoringOtherApps: true)
        progress.startAnimation(nil)
        do {
            try release.verify(package)
            try Data("ready".utf8).write(to: directory.appendingPathComponent("ready"), options: .atomic)
        } catch { fail(error.localizedDescription); return }
        waitTimer = Timer.scheduledTimer(withTimeInterval: 0.2, repeats: true) { [weak self] _ in
            MainActor.assumeIsolated { self?.waitForApp() }
        }
    }
    private func parentIsAlive() -> Bool { kill(parent, 0) == 0 || errno != ESRCH }
    private func waitForApp() {
        let approved = FileManager.default.fileExists(atPath: directory.appendingPathComponent("go").path)
        if !parentIsAlive(), approved {
            waitTimer?.invalidate(); waitTimer = nil
            install()
        } else if Date() > deadline {
            waitTimer?.invalidate(); waitTimer = nil
            fail("pika가 종료되지 않아 업데이트를 중단했습니다. 앱에서 다시 업데이트해 주세요.", canRetry: false)
        }
    }
    @objc private func install() {
        guard !installing else { return }
        guard !parentIsAlive(), FileManager.default.fileExists(atPath: directory.appendingPathComponent("go").path) else {
            fail("pika가 아직 실행 중이거나 업데이트 요청이 취소되었습니다.", canRetry: false); return
        }
        do {
            // A user may have installed a newer build while this window was waiting.
            // Same-version retries repair an interrupted install; newer installs win.
            if let installed = Bundle(url: URL(fileURLWithPath: "/Applications/pika.app"))?
                .object(forInfoDictionaryKey: "CFBundleShortVersionString") as? String {
                guard let current = UpdateVersion(installed), let target = UpdateVersion(release.version), current <= target else {
                    throw UpdateError("이미 더 최신 버전이 설치되어 있거나 버전을 확인할 수 없습니다. pika를 다시 열어 주세요.")
                }
            }
            try release.verify(package)
            let script = try UpdateInstallCommand.appleScript(package: package, hash: release.sha256)
            let process = Process()
            let input = Pipe(), output = Pipe()
            process.executableURL = URL(fileURLWithPath: "/usr/bin/osascript")
            process.arguments = ["-"]
            process.environment = ["PATH": "/usr/bin:/bin:/usr/sbin:/sbin", "HOME": NSHomeDirectory(), "TMPDIR": NSTemporaryDirectory()]
            process.standardInput = input
            process.standardOutput = output
            process.standardError = output
            try process.run()
            installing = true
            retry.isHidden = true; reopen.isHidden = true
            progress.startAnimation(nil)
            label.stringValue = "macOS 관리자 승인을 기다리거나 업데이트를 설치하는 중입니다.\n\n완료되면 pika를 다시 엽니다."
            // Only our fixed script is sent; never interpolate an unquoted file path.
            input.fileHandleForWriting.write(Data(script.utf8))
            try? input.fileHandleForWriting.close()
            DispatchQueue.global(qos: .userInitiated).async {
                let result = output.fileHandleForReading.readDataToEndOfFile()
                process.waitUntilExit()
                let text = String(decoding: result.suffix(8_000), as: UTF8.self)
                let success = process.terminationStatus == 0 && text.trimmingCharacters(in: .whitespacesAndNewlines) == "PIKA_UPDATE_OK"
                DispatchQueue.main.async { [weak self] in self?.finished(success: success, details: text) }
            }
        } catch { fail(error.localizedDescription) }
    }
    private func finished(success: Bool, details: String) {
        installing = false
        progress.stopAnimation(nil)
        let log = FileManager.default.urls(for: .cachesDirectory, in: .userDomainMask)[0]
            .appendingPathComponent("com.alwaysawake.mac/updates", isDirectory: true)
        try? FileManager.default.createDirectory(at: log, withIntermediateDirectories: true)
        try? Data(details.utf8).write(to: log.appendingPathComponent("last-update.log"), options: .atomic)
        if success {
            let installed = Bundle(url: URL(fileURLWithPath: "/Applications/pika.app"))?
                .object(forInfoDictionaryKey: "CFBundleShortVersionString") as? String
            guard installed == release.version else { fail("설치된 앱 버전이 예상과 다릅니다. 다시 시도해 주세요."); return }
            label.stringValue = "업데이트 완료. pika를 여는 중…"
            openApp()
        } else {
            let cancelled = details.contains("(-128)")
            fail(cancelled ? "관리자 승인이 취소되었습니다. 다시 시도하거나 pika를 열 수 있습니다." :
                 "업데이트에 실패했습니다. 설치 파일 일부가 변경되었을 수 있으므로 ‘다시 시도’를 눌러 주세요.\n\n기록: ~/Library/Caches/com.alwaysawake.mac/updates/last-update.log")
        }
    }
    private func fail(_ message: String, canRetry: Bool = true) {
        installing = false
        progress.stopAnimation(nil)
        label.stringValue = message
        retry.isHidden = !canRetry
        reopen.isHidden = false
    }
    @objc private func openApp() {
        guard !installing else { return }
        let config = NSWorkspace.OpenConfiguration()
        config.activates = true
        NSWorkspace.shared.openApplication(at: URL(fileURLWithPath: "/Applications/pika.app"), configuration: config) { _, error in
            DispatchQueue.main.async {
                if let error { self.fail("pika를 열지 못했습니다. \(error.localizedDescription)") }
                else { NSApp.terminate(nil) }
            }
        }
    }
    func windowShouldClose(_ sender: NSWindow) -> Bool { !installing }
    func applicationShouldTerminateAfterLastWindowClosed(_ sender: NSApplication) -> Bool { true }
    func applicationShouldTerminate(_ sender: NSApplication) -> NSApplication.TerminateReply { installing ? .terminateCancel : .terminateNow }
    func applicationWillTerminate(_ notification: Notification) {
        waitTimer?.invalidate()
        try? FileManager.default.removeItem(at: directory)
    }
}

let args = CommandLine.arguments
// Validation-only mode is safe for local and CI package checks; no UI or authorization.
if args.count == 6, args[1] == "--verify-package", let size = Int(args[4]), UpdateVersion(args[5]) != nil {
    do {
        let release = UpdateRelease(version: args[5], url: URL(string: UpdateRelease.repository)!, sha256: args[3], size: size)
        guard UpdateRelease.validHash(args[3]) else { throw UpdateError("Invalid digest") }
        try release.verify(URL(fileURLWithPath: args[2]))
        print("Update package verified; no installation performed")
        exit(0)
    } catch { fputs("\(error.localizedDescription)\n", stderr); exit(1) }
}
guard args.count == 6, let size = Int(args[3]), size > 0, size < 50_000_000,
      let version = UpdateVersion(args[4]), version > UpdateVersion(AppIdentity.version)!,
      UpdateRelease.validHash(args[2]), let parent = Int32(args[5]), parent > 1, parent == getppid() else { exit(2) }
let package = URL(fileURLWithPath: args[1]).standardizedFileURL
let directory = package.deletingLastPathComponent()
let temp = FileManager.default.temporaryDirectory.resolvingSymlinksInPath()
guard directory.deletingLastPathComponent().resolvingSymlinksInPath() == temp,
      directory.lastPathComponent.hasPrefix("pika-update-"),
      package.lastPathComponent == "pika-\(args[4]).pkg" else { exit(2) }
let release = UpdateRelease(version: args[4], url: URL(string: UpdateRelease.repository)!, sha256: args[2], size: size)
MainActor.assumeIsolated {
    let app = NSApplication.shared
    let delegate = UpdateDelegate(package: package, release: release, parent: parent)
    app.delegate = delegate
    withExtendedLifetime(delegate) { app.run() }
}
