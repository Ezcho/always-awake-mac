import AppKit
import SwiftUI

@main
struct RenderPreview {
    @MainActor static func main() throws {
        _ = NSApplication.shared
        let model = AppModel()
        model.monitorOn = true
        let renderer = ImageRenderer(content: ControlView(model: model, snapshot: true))
        renderer.scale = 2
        guard let image = renderer.nsImage,
              let tiff = image.tiffRepresentation,
              let bitmap = NSBitmapImageRep(data: tiff),
              let png = bitmap.representation(using: .png, properties: [:]) else {
            throw AwakeError("Preview could not be rendered")
        }
        try png.write(to: URL(fileURLWithPath: CommandLine.arguments[1]))
    }
}
