import Foundation
import OSLog

// Metadata comes from the official site; packages still require the exact GitHub release URL.
final class UpdateRedirects: NSObject, URLSessionTaskDelegate, @unchecked Sendable {
    static func allowed(_ url: URL?) -> Bool {
        guard let url, url.scheme == "https", url.user == nil, url.password == nil,
              url.port == nil || url.port == 443 else { return false }
        return ["no-sleep-pika.online", "api.github.com", "github.com", "release-assets.githubusercontent.com", "objects.githubusercontent.com"].contains(url.host ?? "")
    }
    func urlSession(_ session: URLSession, task: URLSessionTask,
                    willPerformHTTPRedirection response: HTTPURLResponse, newRequest request: URLRequest,
                    completionHandler: @escaping (URLRequest?) -> Void) {
        completionHandler(Self.allowed(request.url) ? request : nil)
    }
}

enum UpdateDownload {
    private static let logger = Logger(subsystem: AppIdentity.bundleID, category: "Update")
    private static func session() -> URLSession {
        let config = URLSessionConfiguration.ephemeral
        config.timeoutIntervalForRequest = 30
        config.timeoutIntervalForResource = 180
        return URLSession(configuration: config, delegate: UpdateRedirects(), delegateQueue: nil)
    }
    static func release(version: String? = nil, using suppliedSession: URLSession? = nil) async throws -> UpdateRelease {
        if let version, UpdateVersion(version) == nil { throw UpdateError("잘못된 버전입니다.") }
        let suffix = version.map { "tags/v\($0)" } ?? "latest"
        let endpoints = [
            URL(string: "https://no-sleep-pika.online/updates/\(version.map { "v\($0)" } ?? "latest").json")!,
            URL(string: "https://api.github.com/repos/Ezcho/always-awake-mac/releases/\(suffix)")!
        ]
        let session = suppliedSession ?? session()
        defer { if suppliedSession == nil { session.invalidateAndCancel() } }
        var rateLimited = false
        for url in endpoints {
            try Task.checkCancellation()
            var request = URLRequest(url: url, timeoutInterval: 15)
            request.cachePolicy = .reloadIgnoringLocalCacheData
            request.setValue("application/json", forHTTPHeaderField: "Accept")
            request.setValue("pika/\(AppIdentity.version)", forHTTPHeaderField: "User-Agent")
            do {
                let (data, response) = try await session.data(for: request)
                try Task.checkCancellation()
                let http = response as? HTTPURLResponse
                let code = http?.statusCode ?? 0
                logger.notice("Metadata \(url.host ?? "unknown", privacy: .public): HTTP \(code)")
                guard UpdateRedirects.allowed(response.url) else { throw UpdateError("업데이트 서버 주소를 검증하지 못했습니다.") }
                if url.host == "api.github.com", code == 429 || (code == 403 && http?.value(forHTTPHeaderField: "X-RateLimit-Remaining") == "0") {
                    rateLimited = true
                }
                guard code == 200 else { throw UpdateError("업데이트 서버 응답 오류: HTTP \(code)") }
                let release = try UpdateRelease.parse(data)
                guard version == nil || release.version == version else { throw UpdateError("요청한 버전과 다운로드 정보가 다릅니다.") }
                logger.notice("Metadata verified: pika \(release.version, privacy: .public)")
                return release
            } catch {
                if error is CancellationError || (error as? URLError)?.code == .cancelled { throw error }
                // Never log response bodies, user addresses, or credentials.
                logger.error("Metadata \(url.host ?? "unknown", privacy: .public) failed; code \((error as NSError).code)")
            }
        }
        if rateLimited { throw UpdateError("GitHub 업데이트 요청 한도에 도달했습니다. 잠시 후 다시 시도하거나 다운로드 페이지를 이용해 주세요.") }
        throw UpdateError("업데이트 정보를 확인하지 못했습니다. 연결을 확인하고 다시 시도하거나 다운로드 페이지를 이용해 주세요.")
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
