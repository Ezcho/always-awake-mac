import AppKit

/// A small, original pixel pika typing at a laptop. Images are made once, never in the timer.
@MainActor
enum PikaStatusArtwork {
    static let idle = image(frame: 0)
    static let working = (1...2).map { image(frame: $0) }
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

            // B concept: each logical pixel is 2×2 points. Keep the face and
            // laptop readable without widening the crowded 22-point status item.
            let silhouette = [
                "..##.##....",
                ".#######...",
                ".########..",
                ".#####.##..",
                ".########..",
                "..######...",
                "..#####....",
                "..#####....",
                "..#####....",
                "...####...."
            ]
            for (y, row) in silhouette.enumerated() {
                for (x, mark) in row.enumerated() where mark == "#" {
                    pixel(x * 2, y * 2, 2, 2)
                }
            }
            // Bold laptop screen, base and alternating typing paw.
            pixel(18, 10, 4, 2)
            pixel(20, 12, 2, 8)
            pixel(12, 18, 8, 2)
            pixel(2, 20, 20, 2)
            pixel(12, frame == 2 ? 16 : 14, 6, 2)
            if recovery {
                pixel(20, 2, 2, 4)
                pixel(20, 8, 2, 2)
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
