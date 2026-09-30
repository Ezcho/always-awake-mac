import Foundation
import CryptoKit

// Downloads a release-specific application and helper package. It never installs or authorizes
// privileged code: the user completes that step in Apple's Installer.
enum HelperSetupDownload {
    private struct Release: Decodable {
        let tag_name: String
        let draft: Bool
        let assets: [Asset]
    }
    private struct Asset: Decodable {
        let name: String
        let browser_download_url: String
        let digest: String?
        let size: Int
    }

    static func download() async throws -> URL {
        let version = AppIdentity.version
        let filename = "pika-\(version).pkg"
        let expectedURL = "https://github.com/Ezcho/always-awake-mac/releases/download/v\(version)/\(filename)"
        let api = URL(string: "https://api.github.com/repos/Ezcho/always-awake-mac/releases/tags/v\(version)")!
        var request = URLRequest(url: api)
        request.timeoutInterval = 30
        request.setValue("application/vnd.github+json", forHTTPHeaderField: "Accept")
        request.setValue("pika/\(version)", forHTTPHeaderField: "User-Agent")
        let configuration = URLSessionConfiguration.ephemeral
        configuration.timeoutIntervalForResource = 120
        let session = URLSession(configuration: configuration)
        defer { session.invalidateAndCancel() }
        let (data, response) = try await session.data(for: request)
        guard (response as? HTTPURLResponse)?.statusCode == 200, data.count < 2_000_000 else {
            throw AwakeError("pika 다운로드 정보를 가져오지 못했습니다. 인터넷 연결을 확인하고 다시 시도해 주세요.")
        }
        let release = try JSONDecoder().decode(Release.self, from: data)
        guard release.tag_name == "v\(version)", !release.draft,
              let asset = release.assets.first(where: { $0.name == filename }),
              asset.browser_download_url == expectedURL,
              asset.size > 0, asset.size < 10_000_000,
              let digest = asset.digest, digest.hasPrefix("sha256:"), digest.count == 71 else {
            throw AwakeError("현재 앱과 일치하는 pika 설치 파일을 확인하지 못했습니다. 홈페이지에서 최신 앱을 받아 주세요.")
        }
        let (temporary, packageResponse) = try await session.download(from: URL(string: expectedURL)!)
        defer { try? FileManager.default.removeItem(at: temporary) }
        guard (packageResponse as? HTTPURLResponse)?.statusCode == 200,
              packageResponse.url?.scheme == "https",
              let size = try temporary.resourceValues(forKeys: [.fileSizeKey]).fileSize,
              size == asset.size else { throw AwakeError("pika 파일 다운로드가 완료되지 않았습니다.") }
        let bytes = try Data(contentsOf: temporary)
        let hash = SHA256.hash(data: bytes).map { String(format: "%02x", $0) }.joined()
        guard digest == "sha256:\(hash)" else {
            throw AwakeError("pika 파일의 무결성 검사에 실패했습니다. 파일을 실행하지 않았습니다.")
        }
        let directory = FileManager.default.temporaryDirectory
            .appendingPathComponent("pika-helper-\(UUID().uuidString)", isDirectory: true)
        try FileManager.default.createDirectory(at: directory, withIntermediateDirectories: false,
                                             attributes: [.posixPermissions: 0o700])
        let destination = directory.appendingPathComponent(filename)
        try FileManager.default.copyItem(at: temporary, to: destination)
        return destination
    }
}
