import AppKit
MainActor.assumeIsolated {
    try! FileManager.default.createDirectory(atPath: ".build/status-icon-preview", withIntermediateDirectories: true)
    let frames = [PikaStatusArtwork.idle] + PikaStatusArtwork.working + [PikaStatusArtwork.recovery]
    let width = frames.count * 176, height = 220
    let bitmap = NSBitmapImageRep(bitmapDataPlanes: nil, pixelsWide: width, pixelsHigh: height, bitsPerSample: 8, samplesPerPixel: 4, hasAlpha: true, isPlanar: false, colorSpaceName: .deviceRGB, bytesPerRow: width * 4, bitsPerPixel: 32)!
    NSGraphicsContext.saveGraphicsState()
    NSGraphicsContext.current = NSGraphicsContext(bitmapImageRep: bitmap)
    NSColor.white.setFill()
    NSRect(x: 0, y: 0, width: width, height: height).fill()
    NSGraphicsContext.current?.imageInterpolation = .none
    for (index, frame) in frames.enumerated() {
        frame.draw(in: NSRect(x: index * 176, y: 40, width: 176, height: 176), from: .zero, operation: .sourceOver, fraction: 1)
        frame.draw(in: NSRect(x: index * 176 + 77, y: 6, width: 22, height: 22), from: .zero, operation: .sourceOver, fraction: 1)
        precondition(frame.size == NSSize(width: 22, height: 22))
        precondition(frame.isTemplate)
        precondition(frame.representations.count == 2)
    }
    NSGraphicsContext.restoreGraphicsState()
    try! bitmap.representation(using: .png, properties: [:])!.write(to: URL(fileURLWithPath: ".build/status-icon-preview/preview.png"))
    precondition(Set(PikaStatusArtwork.working.map { $0.tiffRepresentation! }).count == 2)
    print("2 unique cached working frames, idle and recovery; 1×/2× template representations verified")
}

MainActor.assumeIsolated {
    // This is an unattached button: no app launch, status-bar insertion, power or Session operations.
    let button = NSStatusBarButton(frame: NSRect(x: 0, y: 0, width: 22, height: 22))
    func animationTimer(_ icon: PikaStatusIcon) -> Timer? {
        let stored = Mirror(reflecting: icon).children.first { $0.label == "timer" }!.value
        return (stored as? Timer)
    }
    func observerCount(_ icon: PikaStatusIcon) -> Int {
        let stored = Mirror(reflecting: icon).children.first { $0.label == "observers" }!.value
        return (stored as! [NSObjectProtocol]).count
    }
    let center = NSWorkspace.shared.notificationCenter
    var icon: PikaStatusIcon? = PikaStatusIcon(button: button)
    weak var weakIcon = icon
    precondition(observerCount(icon!) == 5)
    precondition(animationTimer(icon!) == nil)
    icon!.update(.on)
    if !NSWorkspace.shared.accessibilityDisplayShouldReduceMotion {
        let originalTimer = animationTimer(icon!)!
        for index in 1...1_000 {
            originalTimer.fire()
            precondition(button.image === PikaStatusArtwork.working[index % PikaStatusArtwork.working.count], "Ticks must reuse cached images")
        }
        for _ in 0..<10_000 { icon!.update(.on) }
        precondition(animationTimer(icon!) === originalTimer)
        center.post(name: NSWorkspace.screensDidSleepNotification, object: nil)
        precondition(animationTimer(icon!) == nil && !originalTimer.isValid)
        center.post(name: NSWorkspace.willSleepNotification, object: nil)
        center.post(name: NSWorkspace.screensDidWakeNotification, object: nil)
        precondition(animationTimer(icon!) == nil, "System sleep still blocks animation")
        center.post(name: NSWorkspace.didWakeNotification, object: nil)
        precondition(animationTimer(icon!) != nil)
        for _ in 0..<100 {
            icon!.update(.off)
            precondition(animationTimer(icon!) == nil)
            icon!.update(.on)
            precondition(animationTimer(icon!) != nil)
        }
    } else {
        precondition(animationTimer(icon!) == nil, "Reduce Motion must not animate")
    }
    icon!.update(.recovery)
    precondition(animationTimer(icon!) == nil)
    precondition(button.image === PikaStatusArtwork.recovery)
    icon!.update(.off)
    precondition(button.image === PikaStatusArtwork.idle)
    icon!.invalidate()
    precondition(observerCount(icon!) == 0)
    icon!.update(.on)
    precondition(animationTimer(icon!) == nil)
    icon = nil
    precondition(weakIcon == nil, "Timers and notification callbacks must not retain the icon")
    weakIcon = nil
    var activeIcon: PikaStatusIcon? = PikaStatusIcon(button: button)
    activeIcon!.update(.on)
    weak var weakActive = activeIcon
    weak var weakTimer = animationTimer(activeIcon!)
    activeIcon = nil
    precondition(weakActive == nil, "An active animation must also tear down")
    precondition(weakTimer?.isValid != true)
    weakActive = nil
    weakTimer = nil
    print("Status icon lifecycle passed: 10,000 repeated updates, 100 ON/OFF cycles, sleep/wake, recovery, cleanup")
}
