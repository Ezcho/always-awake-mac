import AppKit

// Packaging artwork only: no windows or Finder automation.
// Keep the dimensions and icon/arrow centers in sync with DMG-layout.py.
let width = 700, height = 500
let bitmap = NSBitmapImageRep(bitmapDataPlanes: nil, pixelsWide: width, pixelsHigh: height,
    bitsPerSample: 8, samplesPerPixel: 4, hasAlpha: true, isPlanar: false,
    colorSpaceName: .deviceRGB, bytesPerRow: 0, bitsPerPixel: 0)!
NSGraphicsContext.saveGraphicsState()
NSGraphicsContext.current = NSGraphicsContext(bitmapImageRep: bitmap)
let ink = NSColor(red: 0.16, green: 0.18, blue: 0.17, alpha: 1)
let secondary = NSColor(red: 0.38, green: 0.40, blue: 0.39, alpha: 1)
let accent = NSColor(red: 0.80, green: 0.46, blue: 0.20, alpha: 1)
NSColor(red: 0.98, green: 0.975, blue: 0.96, alpha: 1).setFill()
NSRect(x: 0, y: 0, width: width, height: height).fill()
func centered(_ value: String, x: CGFloat = 350, y: CGFloat,
              size: CGFloat, weight: NSFont.Weight = .regular, color: NSColor = ink) {
    let attributes: [NSAttributedString.Key: Any] = [
        .font: NSFont.systemFont(ofSize: size, weight: weight), .foregroundColor: color,
    ]
    let text = NSAttributedString(string: value, attributes: attributes)
    text.draw(at: NSPoint(x: x - text.size().width / 2, y: y))
}
centered("pika", y: 441, size: 27, weight: .semibold)
accent.setStroke()
let arrow = NSBezierPath()
arrow.lineWidth = 3
arrow.lineCapStyle = .round
arrow.lineJoinStyle = .round
arrow.move(to: NSPoint(x: 320, y: 355))
arrow.line(to: NSPoint(x: 380, y: 355))
arrow.move(to: NSPoint(x: 370, y: 365))
arrow.line(to: NSPoint(x: 380, y: 355))
arrow.line(to: NSPoint(x: 370, y: 345))
arrow.stroke()

NSColor(red: 0.87, green: 0.87, blue: 0.84, alpha: 1).setFill()
NSRect(x: 44, y: 255, width: 612, height: 1).fill()
centered("1  Drag to Applications", x: 190, y: 215, size: 16, weight: .semibold)
centered("응용 프로그램 폴더로 드래그", x: 190, y: 193, size: 13, color: secondary)
centered("2  Open pika", x: 515, y: 215, size: 16, weight: .semibold)
centered("응용 프로그램에서 pika 실행", x: 515, y: 193, size: 13, color: secondary)

centered("3  Only if macOS blocks opening", y: 143, size: 16, weight: .semibold)
centered("System Settings → Privacy & Security → Open Anyway", y: 112, size: 15)
centered("차단된 경우에만: 시스템 설정 → 개인정보 보호 및 보안 → 그래도 열기", y: 86,
    size: 12, color: secondary)
centered("Check that the app is pika, then approve.  ·  pika인지 확인한 뒤 직접 승인하세요.",
    y: 45, size: 12, color: secondary)
NSGraphicsContext.restoreGraphicsState()
try bitmap.representation(using: .png, properties: [:])!.write(to: URL(fileURLWithPath: CommandLine.arguments[1]))
