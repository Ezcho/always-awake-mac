import AppKit

@MainActor
final class AppDelegate: NSObject, NSApplicationDelegate, NSMenuDelegate {
    let model = AppModel()
    private var statusItem: NSStatusItem!
    private let menu = NSMenu()
    private let sessionRow = MenuSwitchRow(title: "Session")
    private let monitorRow = MenuSwitchRow(title: "Monitor")
    private let setupItem = NSMenuItem(title: "권한 허용…", action: #selector(prepareService), keyEquivalent: "")
    private let errorItem = NSMenuItem(title: "안내…", action: #selector(showMessage), keyEquivalent: "")
    private let removeItem = NSMenuItem(title: "보조 서비스 제거", action: #selector(removeService), keyEquivalent: "")
    private var pendingTermination = false

    func applicationDidFinishLaunching(_ notification: Notification) {
        let peers = NSRunningApplication.runningApplications(withBundleIdentifier: AppIdentity.bundleID)
        if let existing = peers.first(where: { $0.processIdentifier != ProcessInfo.processInfo.processIdentifier }) {
            existing.activate(options: [.activateAllWindows])
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
        menu.addItem(.separator())
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
        statusItem.button?.target = self
        statusItem.button?.action = #selector(statusClick)
        statusItem.button?.sendAction(on: [.leftMouseUp, .rightMouseUp])
        model.onChange = { [weak self] in self?.updateMenu() }
        updateMenu()
        // Show where the app lives when opened from Finder; there is no app window.
        DispatchQueue.main.async { [weak self] in self?.showMenu() }
    }

    @objc func statusClick() {
        if NSApp.currentEvent?.modifierFlags.contains(.option) == true {
            model.toggleSession()
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
        monitorRow.update(on: model.monitorOn, enabled: !model.busy)
        setupItem.isHidden = model.serviceReady
        setupItem.isEnabled = !model.busy
        errorItem.isHidden = model.error == nil && !model.recoveryRequired
        errorItem.title = model.recoveryRequired ? "복구 필요…" : "안내…"
        errorItem.toolTip = model.error
        removeItem.isHidden = !model.serviceReady && !model.needsApproval
        removeItem.isEnabled = !model.busy
        let symbol = model.recoveryRequired ? "exclamationmark.circle" : model.active ? "power.circle.fill" : "power.circle"
        let image = NSImage(systemSymbolName: symbol, accessibilityDescription: "Always Awake \(model.active ? "ON" : "OFF")")
        image?.isTemplate = true
        statusItem?.button?.image = image
        statusItem?.button?.toolTip = "Always Awake · \(model.active ? "ON" : "OFF")\n클릭: 메뉴 · Option+클릭: Session 전환"
    }

    @objc private func toggleSession() { model.toggleSession(); updateMenu() }
    @objc private func toggleMonitor() { model.setMonitor(!model.monitorOn) }
    @objc private func prepareService() { menu.cancelTracking(); model.prepareService() }
    @objc private func removeService() { menu.cancelTracking(); model.removeService() }
    @objc private func openGuide() {
        if let url = Bundle.main.url(forResource: "Guide", withExtension: "html") { NSWorkspace.shared.open(url) }
    }
    @objc private func showMessage() {
        menu.cancelTracking()
        let alert = NSAlert()
        alert.messageText = model.recoveryRequired ? "잠자기 설정 복구" : "Always Awake"
        alert.informativeText = model.error ?? "Session 스위치를 눌러 잠자기 설정을 복구해 주세요."
        alert.addButton(withTitle: "확인")
        NSApp.activate(ignoringOtherApps: true)
        alert.runModal()
    }
    @objc private func quitApp() { menu.cancelTracking(); NSApp.terminate(nil) }
    func applicationShouldHandleReopen(_ sender: NSApplication, hasVisibleWindows flag: Bool) -> Bool { showMenu(); return true }
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
    let app = NSApplication.shared
    let delegate = AppDelegate()
    app.delegate = delegate
    withExtendedLifetime(delegate) { app.run() }
}
