import AppKit

let directory = CommandLine.arguments[1]
try FileManager.default.createDirectory(atPath: directory, withIntermediateDirectories: true)
for size in [16, 32, 64, 128, 256, 512, 1024] {
    let bitmap = NSBitmapImageRep(bitmapDataPlanes: nil, pixelsWide: size, pixelsHigh: size,
        bitsPerSample: 8, samplesPerPixel: 4, hasAlpha: true, isPlanar: false, colorSpaceName: .deviceRGB, bytesPerRow: 0, bitsPerPixel: 0)!
    NSGraphicsContext.saveGraphicsState()
    NSGraphicsContext.current = NSGraphicsContext(bitmapImageRep: bitmap)
    let s = CGFloat(size)
    let rect = NSRect(x: s * 0.04, y: s * 0.04, width: s * 0.92, height: s * 0.92)
    let path = NSBezierPath(roundedRect: rect, xRadius: s * 0.215, yRadius: s * 0.215)
    NSGradient(starting: NSColor(red: 0.12, green: 0.19, blue: 0.16, alpha: 1), ending: NSColor(red: 0.035, green: 0.065, blue: 0.055, alpha: 1))!.draw(in: path, angle: -70)
    let symbol = NSImage(systemSymbolName: "power", accessibilityDescription: nil)!
        .withSymbolConfiguration(.init(pointSize: s * 0.52, weight: .medium))!
    let tinted = NSImage(size: symbol.size)
    tinted.lockFocus()
    NSColor(red: 0.65, green: 0.96, blue: 0.76, alpha: 1).set()
    NSRect(origin: .zero, size: symbol.size).fill()
    symbol.draw(at: .zero, from: .zero, operation: .destinationIn, fraction: 1)
    tinted.unlockFocus()
    tinted.draw(in: NSRect(x: s * 0.255, y: s * 0.24, width: s * 0.49, height: s * 0.52))
    NSGraphicsContext.restoreGraphicsState()
    let data = bitmap.representation(using: .png, properties: [:])!
    let name: String
    switch size {
    case 1024: name = "icon_512x512@2x.png"
    case 64: name = "icon_32x32@2x.png"
    default: name = "icon_\(size)x\(size).png"
    }
    try data.write(to: URL(fileURLWithPath: directory).appendingPathComponent(name))
    if [32, 256, 512].contains(size) {
        try data.write(to: URL(fileURLWithPath: directory).appendingPathComponent("icon_\(size / 2)x\(size / 2)@2x.png"))
    }
}

// ICNS supports embedded PNG representations directly. Avoid iconutil's dependency
// on the system image conversion service in sandboxed build environments.
var representations = Data()
for (kind, filename) in [("icp4", "icon_16x16.png"), ("icp5", "icon_32x32.png"),
                         ("icp6", "icon_32x32@2x.png"), ("ic07", "icon_128x128.png"),
                         ("ic08", "icon_256x256.png"), ("ic09", "icon_512x512.png"),
                         ("ic10", "icon_512x512@2x.png")] {
    let png = try Data(contentsOf: URL(fileURLWithPath: directory).appendingPathComponent(filename))
    representations.append(contentsOf: kind.utf8)
    var length = UInt32(png.count + 8).bigEndian
    withUnsafeBytes(of: &length) { representations.append(contentsOf: $0) }
    representations.append(png)
}
var icns = Data("icns".utf8)
var length = UInt32(representations.count + 8).bigEndian
withUnsafeBytes(of: &length) { icns.append(contentsOf: $0) }
icns.append(representations)
if CommandLine.arguments.count > 2 { try icns.write(to: URL(fileURLWithPath: CommandLine.arguments[2])) }
