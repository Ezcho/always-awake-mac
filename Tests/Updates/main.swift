import Foundation
import CryptoKit

var checks = 0
func check(_ condition: Bool, _ message: String) {
    precondition(condition, message); checks += 1; print("PASS \(message)")
}
func rejected(_ message: String, _ action: () throws -> Void) {
    do { try action(); fatalError("Accepted: \(message)") } catch { checks += 1; print("PASS reject \(message)") }
}
func manifest(version: String = "1.0.10", edits: [String: Any] = [:], assetEdits: [String: Any] = [:], duplicate: Bool = false) throws -> Data {
    var asset: [String: Any] = ["name": "pika-\(version).pkg", "browser_download_url": "\(UpdateRelease.repository)/releases/download/v\(version)/pika-\(version).pkg", "digest": "sha256:" + String(repeating: "a", count: 64), "size": 10]
    asset.merge(assetEdits) { _, new in new }
    var release: [String: Any] = ["tag_name": "v\(version)", "draft": false, "prerelease": false, "assets": duplicate ? [asset, asset] : [asset]]
    release.merge(edits) { _, new in new }
    return try JSONSerialization.data(withJSONObject: release)
}
let release = try UpdateRelease.parse(manifest())
check(release.isNewer(than: "1.0.9"), "numeric 1.0.10 sorts after 1.0.9")
check(!release.isNewer(than: "1.0.10") && !release.isNewer(than: "1.1.0"), "no reinstall or downgrade")
for value in ["1.0", "1.0.1-beta", "01.0.1", "1.-1.0", "1.0.9999999999", "1.0.$(id)", "1.０.1", "v1.0.1", "1.0.1\n"] {
    check(UpdateVersion(value) == nil, "invalid version: \(value.debugDescription)")
}
for edits in [["draft": true], ["prerelease": true], ["tag_name": "latest"]] {
    rejected("unpublished/invalid release") { _ = try UpdateRelease.parse(manifest(edits: edits)) }
}
for edits: [String: Any] in [["browser_download_url": "http://github.com/pika.pkg"], ["browser_download_url": "https://evil.invalid/pika.pkg"], ["digest": "sha256:" + String(repeating: "z", count: 64)], ["digest": NSNull()], ["size": 0], ["size": 50_000_000], ["name": "different.pkg"]] {
    rejected("untrusted asset \(edits.keys)") { _ = try UpdateRelease.parse(manifest(assetEdits: edits)) }
}
rejected("duplicate assets") { _ = try UpdateRelease.parse(manifest(duplicate: true)) }
rejected("oversized metadata") { _ = try UpdateRelease.parse(Data(repeating: 32, count: 2_000_000)) }
for value in ["http://github.com/file", "https://evil.invalid/file", "https://github.com.evil.invalid/file", "https://name@github.com/file", "https://github.com:444/file"] {
    check(!UpdateRedirects.allowed(URL(string: value)), "reject redirect \(value)")
}
check(UpdateRedirects.allowed(URL(string: "https://release-assets.githubusercontent.com/file")), "allow GitHub asset delivery")
let root = URL(fileURLWithPath: ".build/update-tests", isDirectory: true).standardizedFileURL
try FileManager.default.createDirectory(at: root, withIntermediateDirectories: true)
// A shell metacharacter filename exercises the command quoting boundary.
let file = root.appendingPathComponent("pika ' $(touch INJECTED).pkg")
let content = Data("fake package for isolated updater tests".utf8)
try content.write(to: file)
let hash = SHA256.hash(data: content).map { String(format: "%02x", $0) }.joined()
let fixture = UpdateRelease(version: "99.0.0", url: URL(string: UpdateRelease.repository)!, sha256: hash, size: content.count)
try fixture.verify(file); check(true, "matching size and hash accepted")
let link = root.appendingPathComponent("symlink.pkg")
try? FileManager.default.removeItem(at: link)
try FileManager.default.createSymbolicLink(at: link, withDestinationURL: file)
rejected("symlink package") { try fixture.verify(link) }
try Data(repeating: 65, count: content.count).write(to: file)
rejected("tampered same-size package") { try fixture.verify(file) }
try content.write(to: file)
let shell = try UpdateInstallCommand.script(package: file, hash: hash)
check(shell.range(of: "actual=${actual%% *}")!.lowerBound < shell.range(of: "/usr/sbin/installer")!.lowerBound, "root snapshot checked before installer")
check(shell.contains("trap '") && shell.contains("umask 077"), "private staging and cleanup")
try shell.write(to: root.appendingPathComponent("install.sh"), atomically: true, encoding: .utf8)
try UpdateInstallCommand.appleScript(package: file, hash: hash).write(to: root.appendingPathComponent("authorize.applescript"), atomically: true, encoding: .utf8)
rejected("digest injection") { _ = try UpdateInstallCommand.script(package: file, hash: "';id") }
rejected("remote package path") { _ = try UpdateInstallCommand.script(package: URL(string: "https://example.invalid/a")!, hash: hash) }
print("\(checks) update validation checks passed; no administrator prompts or installation")
