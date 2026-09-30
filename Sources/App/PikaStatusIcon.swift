import AppKit

/// A small, original pixel pika typing at a laptop. Images are made once, never in the timer.
@MainActor
enum PikaStatusArtwork {
    static let idle = image(frame: 0)
    static let working = (0..<4).map { image(frame: $0 + 1) }
    static let recovery = image(frame: 0, recovery: true)

    private static func image(frame: Int, recovery: Bool = false) -> NSImage {
        let image = NSImage(size: NSSize(width: 22, height: 22))
        // Explicit 1× / 2× representations keep the tiny pixel silhouette crisp on both displays.
        for scale in [1, 2] {
            let size = 22 * scale
            let bitmap = NSBitmapImageRep(bitmapDataPlanes: nil, pixelsWide: size, pixelsHigh: size,
                bitsPerSample: 8, samplesPerPixel: 4, hasAlpha: true, isPlanar: false,
                colorSpaceName: .deviceRGB, bytesPerRow: size * 4, bitsPerPixel: 32)!
            bitmap.size = NSSize(width: 22, height: 22)
            let context = CGContext(data: bitmap.bitmapData, width: size, height: size,
                bitsPerComponent: 8, bytesPerRow: size * 4, space: CGColorSpaceCreateDeviceRGB(),
                bitmapInfo: CGImageAlphaInfo.premultipliedLast.rawValue)!
            context.clear(CGRect(x: 0, y: 0, width: size, height: size))
            context.scaleBy(x: CGFloat(scale), y: CGFloat(scale))
            context.setShouldAntialias(false)
            context.setFillColor(NSColor.black.cgColor)
            func pixel(_ x: Int, _ y: Int, _ width: Int = 1, _ height: Int = 1, clear: Bool = false) {
                let rect = CGRect(x: x, y: 22 - y - height, width: width, height: height)
                if clear { context.clear(rect) } else { context.fill(rect) }
            }

            // Short round ears, a rounded cheek and a compact body distinguish a pika from a rabbit.
            let bob = frame == 2 || frame == 3 ? 1 : 0
            let head = [
                "..##..##...",
                ".########..",
                ".########..",
                "..########.",
                ".##########",
                ".##########",
                "..########.",
                "...######.."
            ]
            for (y, row) in head.enumerated() {
                for (x, mark) in row.enumerated() where mark == "#" { pixel(x + 1, y + 3 + bob) }
            }
            pixel(4, 5 + bob, clear: true)
            pixel(8, 5 + bob, clear: true)
            pixel(9, 7 + bob, clear: true)
            pixel(3, 11, 7, 1)
            pixel(2, 12, 8, 5)
            pixel(3, 17, 7, 2)
            pixel(1, 15, 2, 2)
            pixel(5, 14, 1, 3, clear: true)
            pixel(7, 18, 4, 1)

            // Angled open laptop and a one-pixel desk. The screen stays hollow at menu-bar size.
            pixel(15, 10, 6)
            pixel(14, 11, 1, 3)
            pixel(13, 14, 1, 3)
            pixel(20, 11, 1, 3)
            pixel(19, 14, 1, 3)
            pixel(14, 16, 5)
            pixel(11, 17, 9)
            pixel(2, 20, 19)
            if frame == 0 {
                pixel(10, 15, 3)
            } else if frame % 2 == 1 {
                pixel(10, 13, 3)
                pixel(10, 16, 2)
            } else {
                pixel(10, 14, 2)
                pixel(11, 15, 2)
            }
            if recovery {
                // A separate exclamation badge remains legible without relying on color.
                pixel(18, 2, 1, 3)
                pixel(18, 6)
            }
            image.addRepresentation(bitmap)
        }
        image.isTemplate = true
        image.accessibilityDescription = recovery ? "pika recovery required" : "Working pika"
        return image
    }
}

@MainActor
final class PikaStatusIcon {
    enum State: Equatable { case off, on, recovery }

    private weak var button: NSStatusBarButton?
    private let center = NSWorkspace.shared.notificationCenter
    private var observers: [NSObjectProtocol] = []
    private var timer: Timer?
    private var state: State?
    private var frameIndex = 0
    private var systemSleeping = false
    private var displaySleeping = false
    private var reduceMotion = NSWorkspace.shared.accessibilityDisplayShouldReduceMotion
    private var invalidated = false

    init(button: NSStatusBarButton) {
        self.button = button
        // Force the finite frame cache to load before the first animation tick.
        _ = PikaStatusArtwork.idle
        _ = PikaStatusArtwork.working
        _ = PikaStatusArtwork.recovery
        observe(NSWorkspace.willSleepNotification) { $0.systemSleeping = true }
        observe(NSWorkspace.didWakeNotification) { $0.systemSleeping = false }
        observe(NSWorkspace.screensDidSleepNotification) { $0.displaySleeping = true }
        observe(NSWorkspace.screensDidWakeNotification) { $0.displaySleeping = false }
        observe(NSWorkspace.accessibilityDisplayOptionsDidChangeNotification) {
            $0.reduceMotion = NSWorkspace.shared.accessibilityDisplayShouldReduceMotion
        }
        update(.off)
    }

    private func observe(_ name: Notification.Name, change: @escaping (PikaStatusIcon) -> Void) {
        observers.append(center.addObserver(forName: name, object: nil, queue: .main) { [weak self] _ in
            MainActor.assumeIsolated {
                guard let self, !self.invalidated else { return }
                change(self)
                self.updateAnimation()
            }
        })
    }

    func update(_ newState: State) {
        guard !invalidated, state != newState else { return }
        state = newState
        frameIndex = 0
        let label: String
        switch newState {
        case .off: label = "pika · Session OFF"; button?.image = PikaStatusArtwork.idle
        case .on: label = "pika · Session ON"; button?.image = PikaStatusArtwork.working[0]
        case .recovery: label = "pika · 복구 필요"; button?.image = PikaStatusArtwork.recovery
        }
        button?.setAccessibilityLabel(label)
        button?.toolTip = label + "\n클릭: 메뉴 · Option+클릭: Session 전환"
        updateAnimation()
    }

    private func updateAnimation() {
        let shouldAnimate = !invalidated && state == .on && !reduceMotion && !systemSleeping && !displaySleeping
        guard shouldAnimate else {
            timer?.invalidate()
            timer = nil
            if state == .on { button?.image = PikaStatusArtwork.working[0] }
            return
        }
        guard timer == nil else { return }
        let timer = Timer(timeInterval: 0.25, repeats: true) { [weak self] _ in
            MainActor.assumeIsolated {
                guard let self else { return }
                self.frameIndex = (self.frameIndex + 1) % PikaStatusArtwork.working.count
                self.button?.image = PikaStatusArtwork.working[self.frameIndex]
            }
        }
        timer.tolerance = 0.025
        RunLoop.main.add(timer, forMode: .common)
        self.timer = timer
    }

    func invalidate() {
        guard !invalidated else { return }
        invalidated = true
        timer?.invalidate()
        timer = nil
        for observer in observers { center.removeObserver(observer) }
        observers.removeAll()
    }

    deinit {
        timer?.invalidate()
        for observer in observers { center.removeObserver(observer) }
    }
}
