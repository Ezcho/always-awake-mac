import AppKit

let directory = CommandLine.arguments[1]
try FileManager.default.createDirectory(atPath: directory, withIntermediateDirectories: true)
let source = NSImage(contentsOfFile: "Resources/PikaAppIcon.png")!
for size in [16, 32, 64, 128, 256, 512, 1024] {
    let bitmap = NSBitmapImageRep(bitmapDataPlanes: nil, pixelsWide: size, pixelsHigh: size,
        bitsPerSample: 8, samplesPerPixel: 4, hasAlpha: true, isPlanar: false, colorSpaceName: .deviceRGB, bytesPerRow: 0, bitsPerPixel: 0)!
    NSGraphicsContext.saveGraphicsState()
    NSGraphicsContext.current = NSGraphicsContext(bitmapImageRep: bitmap)
    NSGraphicsContext.current?.imageInterpolation = .high
    // Apply the consistent macOS icon tile boundary during ICNS export.
    let inset = CGFloat(size) * 0.052
    let tile = NSRect(x: inset, y: inset, width: CGFloat(size) - 2 * inset, height: CGFloat(size) - 2 * inset)
    NSBezierPath(roundedRect: tile, xRadius: CGFloat(size) * 0.205, yRadius: CGFloat(size) * 0.205).addClip()
    source.draw(in: NSRect(x: 0, y: 0, width: size, height: size), from: .zero,
                operation: .copy, fraction: 1)
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
