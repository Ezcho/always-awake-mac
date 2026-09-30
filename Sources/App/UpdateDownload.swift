import Foundation

// Only GitHub HTTPS endpoints belonging to this release flow are accepted.
final class UpdateRedirects: NSObject, URLSessionTaskDelegate, @unchecked Sendable {
    static func allowed(_ url: URL?) -> Bool {
        guard let url, url.scheme == "https", url.user == nil, url.password == nil,
              url.port == nil || url.port == 443 else { return false }
        return ["api.github.com", "github.com", "release-assets.githubusercontent.com", "objects.githubusercontent.com"].contains(url.host ?? "")
    }
    func urlSession(_ session: URLSession, task: URLSessionTask,
                    willPerformHTTPRedirection response: HTTPURLResponse, newRequest request: URLRequest,
                    completionHandler: @escaping (URLRequest?) -> Void) {
        completionHandler(Self.allowed(request.url) ? request : nil)
    }
}

enum UpdateDownload {
    private static func session() -> URLSession {
        let config = URLSessionConfiguration.ephemeral
        config.timeoutIntervalForRequest = 30
        config.timeoutIntervalForResource = 180
        return URLSession(configuration: config, delegate: UpdateRedirects(), delegateQueue: nil)
    }
    static func release(version: String? = nil) async throws -> UpdateRelease {
        if let version, UpdateVersion(version) == nil { throw UpdateError("잘못된 버전입니다.") }
        let suffix = version.map { "tags/v\($0)" } ?? "latest"
        let url = URL(string: "https://api.github.com/repos/Ezcho/always-awake-mac/releases/\(suffix)")!
        var request = URLRequest(url: url)
        request.cachePolicy = .reloadIgnoringLocalCacheData
        request.setValue("application/vnd.github+json", forHTTPHeaderField: "Accept")
        request.setValue("pika/\(AppIdentity.version)", forHTTPHeaderField: "User-Agent")
        let session = session()
        defer { session.invalidateAndCancel() }
        let (data, response) = try await session.data(for: request)
        guard (response as? HTTPURLResponse)?.statusCode == 200, UpdateRedirects.allowed(response.url) else {
            throw UpdateError("업데이트 정보를 가져오지 못했습니다. 인터넷 연결을 확인하고 잠시 후 다시 시도해 주세요.")
        }
        let release = try UpdateRelease.parse(data)
        guard version == nil || release.version == version else { throw UpdateError("요청한 버전과 다운로드 정보가 다릅니다.") }
        return release
    }
    static func package(_ release: UpdateRelease) async throws -> URL {
        let session = session()
        defer { session.invalidateAndCancel() }
        let (temporary, response) = try await session.download(from: release.url)
        defer { try? FileManager.default.removeItem(at: temporary) }
        guard (response as? HTTPURLResponse)?.statusCode == 200, UpdateRedirects.allowed(response.url) else {
            throw UpdateError("업데이트 다운로드에 실패했습니다.")
        }
        try release.verify(temporary)
        let directory = FileManager.default.temporaryDirectory.appendingPathComponent("pika-update-\(UUID().uuidString)", isDirectory: true)
        try FileManager.default.createDirectory(at: directory, withIntermediateDirectories: false, attributes: [.posixPermissions: 0o700])
        do {
            let destination = directory.appendingPathComponent(release.url.lastPathComponent)
            try FileManager.default.copyItem(at: temporary, to: destination)
            return destination
        } catch {
            try? FileManager.default.removeItem(at: directory)
            throw error
        }
    }
}
