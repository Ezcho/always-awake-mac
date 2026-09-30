import Foundation
import CryptoKit

struct UpdateError: LocalizedError {
    let message: String
    init(_ message: String) { self.message = message }
    var errorDescription: String? { message }
}

struct UpdateVersion: Comparable, Equatable {
    let parts: [Int]
    init?(_ value: String) {
        let fields = value.split(separator: ".", omittingEmptySubsequences: false)
        guard fields.count == 3, fields.allSatisfy({ !$0.isEmpty && $0.count <= 6 && $0.allSatisfy({ $0 >= "0" && $0 <= "9" }) }),
              fields.allSatisfy({ $0.count == 1 || $0.first != "0" }) else { return nil }
        parts = fields.map { Int($0)! }
    }
    static func < (lhs: Self, rhs: Self) -> Bool { lhs.parts.lexicographicallyPrecedes(rhs.parts) }
}

struct UpdateRelease: Equatable {
    let version: String
    let url: URL
    let sha256: String
    let size: Int
    static let repository = "https://github.com/Ezcho/always-awake-mac"

    private struct Manifest: Decodable {
        struct Asset: Decodable { let name: String; let browser_download_url: String; let digest: String?; let size: Int }
        let tag_name: String
        let draft: Bool
        let prerelease: Bool
        let assets: [Asset]
    }

    static func parse(_ data: Data) throws -> Self {
        guard data.count < 2_000_000 else { throw UpdateError("업데이트 정보가 너무 큽니다.") }
        let release = try JSONDecoder().decode(Manifest.self, from: data)
        guard release.tag_name.hasPrefix("v"), !release.draft, !release.prerelease else {
            throw UpdateError("정식 공개 버전만 업데이트할 수 있습니다.")
        }
        let version = String(release.tag_name.dropFirst())
        guard UpdateVersion(version) != nil else { throw UpdateError("업데이트 버전을 확인하지 못했습니다.") }
        let filename = "pika-\(version).pkg"
        let expected = "\(repository)/releases/download/v\(version)/\(filename)"
        let matches = release.assets.filter { $0.name == filename }
        guard matches.count == 1, let asset = matches.first, asset.browser_download_url == expected,
              asset.size > 0, asset.size < 50_000_000,
              let digest = asset.digest, digest.hasPrefix("sha256:") else {
            throw UpdateError("공식 업데이트 파일을 확인하지 못했습니다.")
        }
        let hash = String(digest.dropFirst(7))
        guard validHash(hash) else { throw UpdateError("업데이트 파일의 검증 정보가 없습니다.") }
        return Self(version: version, url: URL(string: expected)!, sha256: hash, size: asset.size)
    }

    static func validHash(_ value: String) -> Bool {
        value.count == 64 && value.allSatisfy { ("0"..."9").contains($0) || ("a"..."f").contains($0) }
    }

    func isNewer(than current: String) -> Bool {
        guard let other = UpdateVersion(current), let version = UpdateVersion(version) else { return false }
        return version > other
    }

    func verify(_ file: URL) throws {
        let values = try file.resourceValues(forKeys: [.isRegularFileKey, .isSymbolicLinkKey, .fileSizeKey])
        guard values.isRegularFile == true, values.isSymbolicLink != true, values.fileSize == size else {
            throw UpdateError("업데이트 파일이 완전하지 않습니다.")
        }
        let bytes = try Data(contentsOf: file)
        let actual = SHA256.hash(data: bytes).map { String(format: "%02x", $0) }.joined()
        guard actual == sha256 else { throw UpdateError("업데이트 파일의 무결성 검사에 실패했습니다. 설치하지 않았습니다.") }
    }
}

// The privileged shell sees only a private snapshot whose digest is checked again.
// No password is collected/stored and no resident service accepts an update command.
enum UpdateInstallCommand {
    static func quote(_ value: String) -> String { "'" + value.replacingOccurrences(of: "'", with: "'\\''") + "'" }
    static func script(package: URL, hash: String) throws -> String {
        guard package.isFileURL, UpdateRelease.validHash(hash) else { throw UpdateError("잘못된 업데이트 요청입니다.") }
        return """
        set -eu
        umask 077
        stage=$(/usr/bin/mktemp -d /private/tmp/pika-install.XXXXXXXX)
        trap '/bin/rm -rf "$stage"' EXIT
        /bin/cp \(quote(package.path)) "$stage/update.pkg"
        actual=$(/usr/bin/shasum -a 256 "$stage/update.pkg")
        actual=${actual%% *}
        [ "$actual" = \(quote(hash)) ] || { echo 'Update checksum mismatch' >&2; exit 1; }
        if /usr/sbin/installer -pkg "$stage/update.pkg" -target / >"$stage/install.log" 2>&1; then
            echo 'PIKA_UPDATE_OK'
        else
            /usr/bin/tail -c 4000 "$stage/install.log" >&2
            exit 1
        fi
        """
    }
    static func appleScript(package: URL, hash: String) throws -> String {
        let command = "/bin/bash -c " + quote(try script(package: package, hash: hash))
        let literal = command.replacingOccurrences(of: "\\", with: "\\\\").replacingOccurrences(of: "\"", with: "\\\"").replacingOccurrences(of: "\n", with: "\\n")
        return "do shell script \"\(literal)\" with administrator privileges"
    }
}

// Bundle caches Info.plist; updates must read fresh bytes before and after replacement.
enum UpdateInstalledApp {
    static func version(at app: URL) -> String? {
        guard let bytes = try? Data(contentsOf: app.appendingPathComponent("Contents/Info.plist")),
              let plist = try? PropertyListSerialization.propertyList(from: bytes, format: nil) as? [String: Any],
              let version = plist["CFBundleShortVersionString"] as? String,
              UpdateVersion(version) != nil else { return nil }
        return version
    }
}
