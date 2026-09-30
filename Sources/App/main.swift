import AppKit
import OSLog

@MainActor
final class AppDelegate: NSObject, NSApplicationDelegate, NSMenuDelegate, NSWindowDelegate {
    private let logger = Logger(subsystem: AppIdentity.bundleID, category: "Lifecycle")
    let model = AppModel()
    private let controlServer = LocalControlServer()
    private var statusItem: NSStatusItem!
    private let menu = NSMenu()
    private let sessionRow = MenuSwitchRow(title: "Session")
    private let monitorRow = MenuSwitchRow(title: "Monitor")
    private let setupItem = NSMenuItem(title: "권한 허용…", action: #selector(prepareService), keyEquivalent: "")
    private let errorItem = NSMenuItem(title: "안내…", action: #selector(showMessage), keyEquivalent: "")
    private let removeItem = NSMenuItem(title: "보조 서비스 제거", action: #selector(removeService), keyEquivalent: "")
    private let modeItem = NSMenuItem(title: "", action: nil, keyEquivalent: "")
    private let windowMode = NSTextField(wrappingLabelWithString: "")
    private var pendingTermination = false
    private var controlWindow: NSWindow?
    private let windowSessionRow = MenuSwitchRow(title: "Session")
    private let windowMonitorRow = MenuSwitchRow(title: "Monitor")
    private let windowSetup = NSButton(title: "권한 허용…", target: nil, action: nil)
    private let windowMessage = NSButton(title: "안내…", target: nil, action: nil)

    func applicationDidFinishLaunching(_ notification: Notification) {
        let peers = NSRunningApplication.runningApplications(withBundleIdentifier: AppIdentity.bundleID)
        if let existing = peers.first(where: { $0.processIdentifier != ProcessInfo.processInfo.processIdentifier }) {
            if let url = existing.bundleURL {
                let configuration = NSWorkspace.OpenConfiguration()
                configuration.activates = true
                NSWorkspace.shared.openApplication(at: url, configuration: configuration)
            }
            NSApp.terminate(nil)
            return
        }
        NSApp.setActivationPolicy(.accessory)
        menu.autoenablesItems = false
        menu.delegate = self
        let sessionItem = NSMenuItem(title: "Session", action: #selector(toggleSession), keyEquivalent: "")
        sessionItem.target = self
        sessionItem.view = sessionRow
        menu.addItem(sessionItem)
        let monitorItem = NSMenuItem(title: "Monitor", action: #selector(toggleMonitor), keyEquivalent: "")
        monitorItem.target = self
        monitorItem.view = monitorRow
        menu.addItem(monitorItem)
        sessionRow.action = { [weak self] in self?.toggleSession() }
        monitorRow.action = { [weak self] in self?.toggleMonitor() }
        modeItem.isEnabled = false
        menu.addItem(modeItem)
        menu.addItem(.separator())
        let openItem = NSMenuItem(title: "제어창 열기", action: #selector(showControlWindow), keyEquivalent: "")
        openItem.target = self
        menu.addItem(openItem)
        for item in [setupItem, errorItem] { item.target = self; menu.addItem(item) }

        let settingsItem = NSMenuItem(title: "설정", action: nil, keyEquivalent: "")
        let settings = NSMenu()
        settings.autoenablesItems = false
        let guide = NSMenuItem(title: "사용 안내", action: #selector(openGuide), keyEquivalent: "")
        guide.target = self
        settings.addItem(guide)
        removeItem.target = self
        settings.addItem(removeItem)
        settingsItem.submenu = settings
        menu.addItem(settingsItem)
        let quit = NSMenuItem(title: "종료", action: #selector(quitApp), keyEquivalent: "q")
        quit.target = self
        menu.addItem(quit)

        statusItem = NSStatusBar.system.statusItem(withLength: NSStatusItem.squareLength)
        statusItem.autosaveName = "AlwaysAwake"
        statusItem.isVisible = true
        logger.notice("Menu bar item created")
        statusItem.button?.target = self
        statusItem.button?.action = #selector(statusClick)
        statusItem.button?.sendAction(on: [.leftMouseUp, .rightMouseUp])
        model.onChange = { [weak self] in self?.updateMenu() }
        do {
            try controlServer.start { [weak self] request, reply in
                MainActor.assumeIsolated {
                    guard let self else { reply(ControlWire.failure("app_closed", "pika is closing")); return }
                    self.model.handleAutomation(request, completion: reply)
                }
            }
        } catch { logger.error("MCP local control unavailable: \(error.localizedDescription)") }
        updateMenu()
        showControlWindow()
    }

    @objc private func showControlWindow() {
        if controlWindow == nil {
            let window = NSWindow(contentRect: NSRect(x: 0, y: 0, width: 264, height: 184),
                                  styleMask: [.titled, .closable, .miniaturizable], backing: .buffered, defer: false)
            window.title = "pika"
            window.delegate = self
            window.isReleasedWhenClosed = false
            window.collectionBehavior = [.moveToActiveSpace]
            window.center()
            windowSessionRow.frame.origin = NSPoint(x: 24, y: 132)
            windowMonitorRow.frame.origin = NSPoint(x: 24, y: 92)
            windowSessionRow.action = { [weak self] in self?.toggleSession() }
            windowMonitorRow.action = { [weak self] in self?.toggleMonitor() }
            windowSetup.target = self
            windowSetup.action = #selector(prepareService)
            windowMessage.target = self
            windowMessage.action = #selector(showMessage)
            for (button, x) in [(windowSetup, CGFloat(24)), (windowMessage, CGFloat(144))] {
                button.bezelStyle = .rounded
                button.controlSize = .small
                button.frame = NSRect(x: x, y: 12, width: 100, height: 26)
            }
            windowMode.font = .systemFont(ofSize: 11)
            windowMode.textColor = .secondaryLabelColor
            windowMode.frame = NSRect(x: 24, y: 46, width: 216, height: 34)
            for view in [windowSessionRow, windowMonitorRow, windowSetup, windowMessage, windowMode] as [NSView] {
                window.contentView?.addSubview(view)
            }
            controlWindow = window
        }
        updateMenu()
        NSApp.activate(ignoringOtherApps: true)
        controlWindow?.makeKeyAndOrderFront(nil)
        logger.notice("Control window opened")
    }

    func windowWillClose(_ notification: Notification) {
        logger.notice("Control window closed; app remains running")
    }

    @objc func statusClick() {
        if NSApp.currentEvent?.modifierFlags.contains(.option) == true {
            toggleSession()
        } else { showMenu() }
    }

    private func showMenu() {
        guard let button = statusItem?.button else { return }
        statusItem.menu = menu
        button.performClick(nil)
        statusItem.menu = nil
    }

    func menuWillOpen(_ menu: NSMenu) { model.refreshService(); updateMenu() }

    private func updateMenu() {
        sessionRow.update(on: model.active, enabled: !model.busy)
        monitorRow.update(on: model.monitorOn, enabled: model.active && !model.busy)
        windowSessionRow.update(on: model.active, enabled: !model.busy)
        windowMonitorRow.update(on: model.monitorOn, enabled: model.active && !model.busy)
        let notice = model.sessionNotice ?? ""
        windowMode.stringValue = notice
        modeItem.title = notice
        modeItem.isHidden = notice.isEmpty
        modeItem.toolTip = notice
        windowSetup.isHidden = model.serviceReady
        windowSetup.isEnabled = !model.busy
        windowMessage.isHidden = model.error == nil && !model.recoveryRequired
        windowMessage.title = model.recoveryRequired ? "복구 필요…" : "안내…"
        setupItem.isHidden = model.serviceReady
        setupItem.isEnabled = !model.busy
        errorItem.isHidden = model.error == nil && !model.recoveryRequired
        errorItem.title = model.recoveryRequired ? "복구 필요…" : "안내…"
        errorItem.toolTip = model.error
        removeItem.isHidden = !model.serviceReady && !model.needsApproval
        removeItem.isEnabled = !model.busy
        let symbol = model.recoveryRequired ? "exclamationmark.circle" : model.active ? "power.circle.fill" : "power.circle"
        let image = NSImage(systemSymbolName: symbol, accessibilityDescription: "pika \(model.active ? "ON" : "OFF")")
        image?.isTemplate = true
        statusItem?.button?.image = image
        statusItem?.button?.toolTip = "pika · \(model.active ? "ON" : "OFF")\n클릭: 메뉴 · Option+클릭: Session 전환"
    }

    @objc private func toggleSession() {
        guard !model.busy else { return }
        // End menu tracking before starting XPC work or presenting an approval/error.
        menu.cancelTracking()
        DispatchQueue.main.async { [weak self] in
            guard let self else { return }
            self.logger.notice("Session toggle requested")
            self.model.toggleSession { [weak self] in
                guard let self else { return }
                self.updateMenu()
                self.logger.notice("Session toggle completed: active=\(self.model.active)")
                if self.model.error != nil {
                    self.showControlWindow()
                    self.showMessage()
                }
            }
        }
    }
    @objc private func toggleMonitor() { model.setMonitor(!model.monitorOn) }
    @objc private func prepareService() { menu.cancelTracking(); model.prepareService() }
    @objc private func removeService() { menu.cancelTracking(); model.removeService() }
    @objc private func openGuide() {
        if let url = Bundle.main.url(forResource: "Guide", withExtension: "html") { NSWorkspace.shared.open(url) }
    }
    @objc private func showMessage() {
        menu.cancelTracking()
        let alert = NSAlert()
        alert.messageText = model.recoveryRequired ? "잠자기 설정 복구" : "pika"
        alert.informativeText = model.error ?? "Session 스위치를 눌러 잠자기 설정을 복구해 주세요."
        alert.addButton(withTitle: "확인")
        NSApp.activate(ignoringOtherApps: true)
        alert.runModal()
    }
    @objc private func quitApp() { menu.cancelTracking(); NSApp.terminate(nil) }
    func applicationShouldHandleReopen(_ sender: NSApplication, hasVisibleWindows flag: Bool) -> Bool { showControlWindow(); return true }
    func applicationShouldTerminateAfterLastWindowClosed(_ sender: NSApplication) -> Bool { false }

    func applicationShouldTerminate(_ sender: NSApplication) -> NSApplication.TerminateReply {
        guard model.active || model.recoveryRequired || model.busy else { model.client.invalidate(); return .terminateNow }
        guard !pendingTermination else { return .terminateCancel }
        if model.busy { return .terminateCancel }
        pendingTermination = true
        model.stop { [weak self] success in
            self?.pendingTermination = false
            sender.reply(toApplicationShouldTerminate: success)
            if !success { self?.showMenu() }
        }
        return .terminateLater
    }
}

MainActor.assumeIsolated {
    if CommandLine.arguments.contains("--unregister-service") {
        ServiceDiagnostics.unregisterLegacyService()
        RunLoop.main.run()
        exit(1)
    }
    if CommandLine.arguments.contains("--repair-service") {
        ServiceDiagnostics.repairRegistration()
        RunLoop.main.run()
        exit(1)
    }
    if CommandLine.arguments.contains("--check-service") || CommandLine.arguments.contains("--test-session") {
        ServiceDiagnostics.run(testSession: CommandLine.arguments.contains("--test-session"))
        RunLoop.main.run()
        exit(1)
    }
    let app = NSApplication.shared
    let delegate = AppDelegate()
    app.delegate = delegate
    withExtendedLifetime(delegate) { app.run() }
}
