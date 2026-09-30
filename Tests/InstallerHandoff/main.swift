import AppKit
import CryptoKit

@main struct HandoffTests {
    @MainActor static func main() async throws {
        let root = FileManager.default.temporaryDirectory.appendingPathComponent("pika-handoff-tests-\(UUID().uuidString)")
        let files = FileManager.default
        try files.createDirectory(at: root, withIntermediateDirectories: true)
        defer { try? files.removeItem(at: root) }
        let source = root.appendingPathComponent("source.pkg")
        let data = Data("isolated native Installer handoff fixture".utf8)
        try data.write(to: source)
        let hash = SHA256.hash(data: data).map { String(format: "%02x", $0) }.joined()
        let release = UpdateRelease(version: "1.0.13", url: URL(string: "\(UpdateRelease.repository)/releases/download/v1.0.13/pika-1.0.13.pkg")!, sha256: hash, size: data.count)
        let app = root.appendingPathComponent("installed.app")
        try files.createDirectory(at: app.appendingPathComponent("Contents"), withIntermediateDirectories: true)
        func installed(_ version: String) throws {
            try PropertyListSerialization.data(fromPropertyList: ["CFBundleShortVersionString": version], format: .xml, options: 0)
                .write(to: app.appendingPathComponent("Contents/Info.plist"))
        }
        try installed("1.0.12")
        let cache = root.appendingPathComponent("cache")
        let retained = try UpdatePackageStore.retain(source, release: release, in: cache)
        var checks = 0
        func check(_ condition: Bool, _ text: String) { precondition(condition, text); checks += 1; print("PASS \(text)") }
        check(retained.lastPathComponent == "pika-1.0.13.pkg", "stable identifiable installer filename")
        check(try UpdatePackageStore.retain(source, release: release, in: cache) == retained, "retry reuses exactly the same file")
        check((try files.attributesOfItem(atPath: cache.path)[.posixPermissions] as? NSNumber)?.intValue == 0o700, "private cache directory")
        try files.removeItem(at: source)
        try release.verify(retained)
        check(true, "package survives temporary download cleanup")
        var calls = 0
        var appExited = false
        do {
            try await SystemInstallerHandoff.open(retained, release: release, installedApp: app) { package, installer in
                calls += 1
                check(package == retained && installer.path == "/System/Library/CoreServices/Installer.app", "explicit Apple Installer gets verified PKG")
                throw NSError(domain: NSOSStatusErrorDomain, code: -10826)
            }
            appExited = true // Caller performs handoff only after a successful open.
            fatalError("Unexpected open success")
        } catch {
            check(!appExited && error.localizedDescription.contains("설치 파일 보기"), "blocked open keeps app alive and explains retry")
        }
        check(files.fileExists(atPath: retained.path), "blocked open does not delete package awaiting approval")
        try await SystemInstallerHandoff.open(retained, release: release, installedApp: app) { package, _ in
            calls += 1; check(package == retained, "approval retry uses retained package")
        }
        check(calls == 2, "open resumes after failure without launching a custom binary")
        try installed("1.0.14")
        do {
            try await SystemInstallerHandoff.open(retained, release: release, installedApp: app) { _, _ in fatalError("Downgrade reached Installer") }
            fatalError("Accepted downgrade")
        } catch { check(true, "newer installed app blocks delayed old package handoff") }
        try installed("1.0.13")
        try await SystemInstallerHandoff.open(retained, release: release, installedApp: app) { _, _ in }
        check(true, "same version remains available for interrupted-install repair")
        try installed("invalid")
        do {
            try await SystemInstallerHandoff.open(retained, release: release, installedApp: app) { _, _ in fatalError("Invalid app reached Installer") }
            fatalError("Accepted malformed installed metadata")
        } catch { check(true, "unreadable installed version fails closed") }
        try installed("1.0.12")
        try Data(repeating: 65, count: data.count).write(to: retained)
        do {
            try await SystemInstallerHandoff.open(retained, release: release, installedApp: app) { _, _ in fatalError("Tampered package reached Installer") }
            fatalError("Accepted tampered package")
        } catch { check(true, "retained package reverified before every open") }
        try data.write(to: source)
        let link = root.appendingPathComponent("linked-cache")
        try files.createSymbolicLink(at: link, withDestinationURL: cache)
        do { _ = try UpdatePackageStore.retain(source, release: release, in: link); fatalError("Accepted symlink cache") }
        catch { check(true, "symlink cache rejected") }
        print("\(checks) native Installer handoff checks; no Installer launched and no power changes")
    }
}
