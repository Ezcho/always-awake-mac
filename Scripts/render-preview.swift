import AppKit

// Render the actual AppKit switch views for the download page, without a live session.
@main
struct RenderPreview {
    @MainActor static func main() throws {
        _ = NSApplication.shared
        let view = NSView(frame: NSRect(x: 0, y: 0, width: 232, height: 80))
        view.wantsLayer = true
        view.layer?.backgroundColor = NSColor.windowBackgroundColor.cgColor
        view.appearance = NSAppearance(named: .aqua)
        let session = MenuSwitchRow(title: "Session")
        session.frame.origin = NSPoint(x: 8, y: 40)
        session.update(on: false, enabled: true)
        let monitor = MenuSwitchRow(title: "Monitor")
        monitor.frame.origin = NSPoint(x: 8, y: 8)
        monitor.update(on: false, enabled: false)
        view.addSubview(session)
        view.addSubview(monitor)
        let window = NSWindow(contentRect: view.frame, styleMask: .borderless, backing: .buffered, defer: false)
        window.contentView = view
        view.layoutSubtreeIfNeeded()
        view.displayIfNeeded()
        guard let bitmap = view.bitmapImageRepForCachingDisplay(in: view.bounds) else { fatalError("Cannot render menu controls") }
        view.cacheDisplay(in: view.bounds, to: bitmap)
        guard let png = bitmap.representation(using: .png, properties: [:]) else { fatalError("Cannot encode preview") }
        try png.write(to: URL(fileURLWithPath: CommandLine.arguments[1]))
    }
}
