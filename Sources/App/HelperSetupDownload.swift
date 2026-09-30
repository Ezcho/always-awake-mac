import Foundation

// Repair always fetches the matching version; updates use the separate latest-release flow.
enum HelperSetupDownload {
    static func download() async throws -> URL {
        try await UpdateDownload.package(UpdateDownload.release(version: AppIdentity.version))
    }
}
