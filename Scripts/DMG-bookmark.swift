import Foundation
import CoreFoundation

// Foundation owns the bookmark format. Hand-written bookmarks can stop resolving
// after the image is detached and mounted at a different path.
do {
    let mode = CommandLine.arguments[1]
    let source = URL(fileURLWithPath: CommandLine.arguments[2])
    if mode == "create" {
        let destination = URL(fileURLWithPath: CommandLine.arguments[3])
        let data = try source.bookmarkData(options: [.suitableForBookmarkFile],
            includingResourceValuesForKeys: nil, relativeTo: nil)
        try data.write(to: destination)
    } else if mode == "verify" || mode == "verify-alias" {
        var stale = false
        var data = try Data(contentsOf: source)
        if mode == "verify-alias" {
            guard let converted = CFURLCreateBookmarkDataFromAliasRecord(nil, data as CFData)?.takeRetainedValue() else {
                throw CocoaError(.fileReadCorruptFile)
            }
            data = converted as Data
        }
        let resolved = try URL(resolvingBookmarkData: data,
            options: [.withoutUI, .withoutMounting], relativeTo: nil,
            bookmarkDataIsStale: &stale)
        guard FileManager.default.fileExists(atPath: resolved.path) else {
            throw CocoaError(.fileNoSuchFile)
        }
        print("Background bookmark resolves:", resolved.path)
    } else {
        throw CocoaError(.fileReadInvalidFileName)
    }
} catch {
    fputs("DMG bookmark: \(error.localizedDescription)\n", stderr)
    exit(1)
}
