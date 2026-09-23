import AppKit
import SwiftUI

@MainActor
final class AppDelegate: NSObject, NSApplicationDelegate, NSWindowDelegate {
    let model = AppModel()
    private var statusItem: NSStatusItem!
    private var window: NSWindow!
    private var pendingTermination = false

    func applicationDidFinishLaunching(_ notification: Notification) {
        // Reopen the existing app instead of allowing competing session owners.
        let peers = NSRunningApplication.runningApplications(withBundleIdentifier: AppIdentity.bundleID)
        if let existing = peers.first(where: { $0.processIdentifier != ProcessInfo.processInfo.processIdentifier }) {
            existing.activate(options: [.activateAllWindows])
            NSApp.terminate(nil)
            return
        }
        NSApp.setActivationPolicy(.accessory)
        statusItem = NSStatusBar.system.statusItem(withLength: NSStatusItem.variableLength)
        if let button = statusItem.button {
            button.target = self
            button.action = #selector(statusClick)
            button.sendAction(on: [.leftMouseUp, .rightMouseUp])
        }
        model.onChange = { [weak self] in self?.updateStatus() }
        updateStatus()

        window = NSWindow(contentRect: NSRect(x: 0, y: 0, width: 400, height: 700),
                          styleMask: [.titled, .closable, .fullSizeContentView], backing: .buffered, defer: false)
        window.title = "Always Awake"
        window.titlebarAppearsTransparent = true
        window.titleVisibility = .hidden
        window.isMovableByWindowBackground = true
        window.isReleasedWhenClosed = false
        window.delegate = self
        window.backgroundColor = NSColor(red: 0.055, green: 0.075, blue: 0.071, alpha: 1)
        window.contentView = NSHostingView(rootView: ControlView(model: model))
        window.center()
        showWindow()
    }

    @objc func statusClick() {
        if NSApp.currentEvent?.type == .rightMouseUp || NSApp.currentEvent?.modifierFlags.contains(.option) == true {
            showWindow()
        } else if !model.serviceReady {
            showWindow()
        } else {
            model.toggleSession()
            if model.error != nil { showWindow() }
        }
    }

    func updateStatus() {
        let symbol = model.active ? "power.circle.fill" : "power.circle"
        let image = NSImage(systemSymbolName: symbol, accessibilityDescription: model.active ? "Always Awake ON" : "Always Awake OFF")
        image?.isTemplate = true
        statusItem?.button?.image = image
        statusItem?.button?.title = model.active ? " ON" : ""
        statusItem?.button?.toolTip = "Always Awake · \(model.active ? "ON" : "OFF")\n클릭: 세션 전환 / 우클릭: 설정"
    }

    func showWindow() { window?.makeKeyAndOrderFront(nil); NSApp.activate(ignoringOtherApps: true) }
    func applicationShouldHandleReopen(_ sender: NSApplication, hasVisibleWindows flag: Bool) -> Bool { showWindow(); return true }
    func applicationShouldTerminateAfterLastWindowClosed(_ sender: NSApplication) -> Bool { false }

    func applicationShouldTerminate(_ sender: NSApplication) -> NSApplication.TerminateReply {
        guard model.active || model.recoveryRequired || model.busy else { model.client.invalidate(); return .terminateNow }
        guard !pendingTermination else { return .terminateCancel }
        if model.busy { showWindow(); return .terminateCancel }
        pendingTermination = true
        model.stop { [weak self] success in
            self?.pendingTermination = false
            if !success { self?.showWindow() }
            sender.reply(toApplicationShouldTerminate: success)
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
