import AppKit
import OSLog

// Use Apple's existing Installer rather than extracting a new executable that
// Gatekeeper may block independently of the app the user already approved.
@MainActor
enum SystemInstallerHandoff {
    static let installer = URL(fileURLWithPath: "/System/Library/CoreServices/Installer.app")
    private static let logger = Logger(subsystem: AppIdentity.bundleID, category: "Update")
    static func open(_ package: URL, release: UpdateRelease,
                     installedApp: URL = URL(fileURLWithPath: "/Applications/pika.app"),
                     opener: (URL, URL) async throws -> Void = launchInstaller) async throws {
        if FileManager.default.fileExists(atPath: installedApp.path) {
            guard let value = UpdateInstalledApp.version(at: installedApp),
                  let current = UpdateVersion(value), let target = UpdateVersion(release.version), current <= target else {
                throw UpdateError("이미 더 최신 버전이 설치되었거나 설치된 버전을 확인할 수 없습니다.")
            }
        }
        try release.verify(package)
        do {
            try await opener(package, installer)
            logger.notice("System Installer opened for pika \(release.version, privacy: .public); installation not yet confirmed")
        } catch {
            logger.error("System Installer open failed; code \((error as NSError).code). Verified package retained.")
            throw UpdateError("macOS 설치 프로그램을 열지 못했습니다. ‘설치 파일 보기’에서 PKG를 다시 여세요. 보안 경고가 있으면 해당 파일을 허용한 뒤 재시도하세요.")
        }
    }
    private static func launchInstaller(_ package: URL, _ installer: URL) async throws {
        let configuration = NSWorkspace.OpenConfiguration()
        configuration.activates = true
        try await withCheckedThrowingContinuation { (continuation: CheckedContinuation<Void, Error>) in
            NSWorkspace.shared.open([package], withApplicationAt: installer, configuration: configuration) { _, error in
                if let error { continuation.resume(throwing: error) }
                else { continuation.resume() }
            }
        }
    }
}

// Keep the same file across blocked launches and retries. Approval is not useful
// if the executable/PKG being approved has already been deleted or moved.
enum UpdatePackageStore {
    static var directory: URL {
        FileManager.default.urls(for: .cachesDirectory, in: .userDomainMask)[0]
            .appendingPathComponent("com.alwaysawake.mac/updates/packages", isDirectory: true)
    }
    static func retain(_ source: URL, release: UpdateRelease, in directory: URL = directory) throws -> URL {
        guard UpdateVersion(release.version) != nil else { throw UpdateError("잘못된 버전입니다.") }
        try release.verify(source)
        let files = FileManager.default
        try files.createDirectory(at: directory, withIntermediateDirectories: true, attributes: [.posixPermissions: 0o700])
        let values = try directory.resourceValues(forKeys: [.isDirectoryKey, .isSymbolicLinkKey])
        guard values.isDirectory == true, values.isSymbolicLink != true else { throw UpdateError("업데이트 저장 위치를 확인하지 못했습니다.") }
        let destination = directory.appendingPathComponent("pika-\(release.version).pkg")
        if files.fileExists(atPath: destination.path) {
            try release.verify(destination)
            return destination
        }
        try files.copyItem(at: source, to: destination)
        do { try release.verify(destination) }
        catch { try? files.removeItem(at: destination); throw error }
        return destination
    }
}
