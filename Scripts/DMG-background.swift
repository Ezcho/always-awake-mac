import AppKit

// Packaging artwork only: no windows or Finder automation.
let width = 600, height = 360
let bitmap = NSBitmapImageRep(bitmapDataPlanes: nil, pixelsWide: width, pixelsHigh: height,
    bitsPerSample: 8, samplesPerPixel: 4, hasAlpha: true, isPlanar: false,
    colorSpaceName: .deviceRGB, bytesPerRow: 0, bitsPerPixel: 0)!
NSGraphicsContext.saveGraphicsState()
NSGraphicsContext.current = NSGraphicsContext(bitmapImageRep: bitmap)
NSColor(red: 0.98, green: 0.975, blue: 0.96, alpha: 1).setFill()
NSRect(x: 0, y: 0, width: width, height: height).fill()
func centered(_ value: String, y: CGFloat, font: NSFont, color: NSColor) {
    let attributes: [NSAttributedString.Key: Any] = [.font: font, .foregroundColor: color]
    let text = NSAttributedString(string: value, attributes: attributes)
    text.draw(at: NSPoint(x: (600 - text.size().width) / 2, y: y))
}
centered("pika", y: 282, font: .systemFont(ofSize: 27, weight: .semibold),
    color: NSColor(red: 0.16, green: 0.18, blue: 0.17, alpha: 1))
centered("Drag to Applications", y: 48, font: .systemFont(ofSize: 15, weight: .medium),
    color: NSColor(red: 0.38, green: 0.40, blue: 0.39, alpha: 1))
NSColor(red: 0.80, green: 0.46, blue: 0.20, alpha: 1).setStroke()
let arrow = NSBezierPath()
arrow.lineWidth = 3
arrow.lineCapStyle = .round
arrow.lineJoinStyle = .round
arrow.move(to: NSPoint(x: 275, y: 190))
arrow.line(to: NSPoint(x: 325, y: 190))
arrow.move(to: NSPoint(x: 315, y: 200))
arrow.line(to: NSPoint(x: 325, y: 190))
arrow.line(to: NSPoint(x: 315, y: 180))
arrow.stroke()
NSGraphicsContext.restoreGraphicsState()
try bitmap.representation(using: .png, properties: [:])!.write(to: URL(fileURLWithPath: CommandLine.arguments[1]))
