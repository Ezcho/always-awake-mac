import Foundation

final class StubProtocol: URLProtocol {
    static var requests: [URLRequest] = []
    static var respond: (URLRequest) throws -> (Int, [String: String], Data) = { _ in fatalError("Unexpected request") }
    override class func canInit(with request: URLRequest) -> Bool { true }
    override class func canonicalRequest(for request: URLRequest) -> URLRequest { request }
    override func startLoading() {
        Self.requests.append(request)
        do {
            let (status, headers, data) = try Self.respond(request)
            let response = HTTPURLResponse(url: request.url!, statusCode: status, httpVersion: "HTTP/1.1", headerFields: headers)!
            client?.urlProtocol(self, didReceive: response, cacheStoragePolicy: .notAllowed)
            client?.urlProtocol(self, didLoad: data)
            client?.urlProtocolDidFinishLoading(self)
        } catch { client?.urlProtocol(self, didFailWithError: error) }
    }
    override func stopLoading() {}
}

@main struct DownloadTests {
    static func manifest(_ version: String = "1.0.12", digest: String = String(repeating: "a", count: 64)) throws -> Data {
        try JSONSerialization.data(withJSONObject: [
            "tag_name": "v\(version)", "draft": false, "prerelease": false,
            "assets": [["name": "pika-\(version).pkg", "size": 100,
                        "browser_download_url": "\(UpdateRelease.repository)/releases/download/v\(version)/pika-\(version).pkg",
                        "digest": "sha256:\(digest)"]]
        ])
    }
    static func main() async throws {
        let config = URLSessionConfiguration.ephemeral
        config.protocolClasses = [StubProtocol.self]
        let session = URLSession(configuration: config)
        defer { session.invalidateAndCancel() }
        let good = try manifest()
        var checks = 0
        func check(_ value: Bool, _ label: String) {
            precondition(value, label); checks += 1; print("PASS \(label)")
        }
        // No API request at all, even if the API quota is exhausted.
        StubProtocol.respond = { request in
            precondition(request.url!.host == "no-sleep-pika.online")
            return (200, [:], good)
        }
        let latest = try await UpdateDownload.release(using: session)
        check(latest.version == "1.0.12" && StubProtocol.requests.count == 1, "official static feed works without GitHub API")
        check(StubProtocol.requests[0].url!.path == "/updates/latest.json", "latest feed path")
        check(StubProtocol.requests[0].cachePolicy == .reloadIgnoringLocalCacheData, "request fresh metadata")
        check(StubProtocol.requests[0].value(forHTTPHeaderField: "Authorization") == nil, "no embedded token")
        StubProtocol.requests = []
        _ = try await UpdateDownload.release(version: "1.0.12", using: session)
        check(StubProtocol.requests[0].url!.path == "/updates/v1.0.12.json", "helper repair uses immutable version feed")
        for failure in ["404", "timeout", "invalid", "digest", "mismatch"] {
            StubProtocol.requests = []
            StubProtocol.respond = { request in
                if request.url!.host == "api.github.com" { return (200, [:], good) }
                switch failure {
                case "404": return (404, [:], Data())
                case "timeout": throw URLError(.timedOut)
                case "invalid": return (200, [:], Data("not JSON".utf8))
                case "digest": return (200, [:], try manifest(digest: "bad"))
                default: return (200, [:], try manifest("1.0.11"))
                }
            }
            let result = try await UpdateDownload.release(version: "1.0.12", using: session)
            check(result == latest && StubProtocol.requests.count == 2, "validated fallback for \(failure)")
            check(StubProtocol.requests[1].url!.path.hasSuffix("/tags/v1.0.12"), "fallback preserves pinned version: \(failure)")
        }
        for status in [403, 429] {
            StubProtocol.respond = { request in
                request.url!.host == "api.github.com" ? (status, ["X-RateLimit-Remaining": "0"], Data()) : (503, [:], Data())
            }
            do { _ = try await UpdateDownload.release(using: session); fatalError("Accepted rate limit") }
            catch { check(error.localizedDescription.contains("요청 한도"), "HTTP \(status) quota error is actionable") }
        }
        StubProtocol.respond = { _ in throw URLError(.notConnectedToInternet) }
        do { _ = try await UpdateDownload.release(using: session); fatalError("Accepted offline") }
        catch { check(error.localizedDescription.contains("다운로드 페이지"), "offline error provides alternate action") }
        StubProtocol.respond = { _ in (200, [:], try manifest(digest: "invalid")) }
        do { _ = try await UpdateDownload.release(using: session); fatalError("Accepted bad hashes") }
        catch { check(true, "all invalid manifests rejected") }
        StubProtocol.requests = []
        do { _ = try await UpdateDownload.release(version: "../latest", using: session); fatalError("Accepted invalid version") }
        catch { check(StubProtocol.requests.isEmpty, "invalid version rejected before network") }
        StubProtocol.respond = { _ in throw URLError(.cancelled) }
        do { _ = try await UpdateDownload.release(using: session); fatalError("Ignored cancellation") }
        catch { check(StubProtocol.requests.count == 1, "cancelled request does not initiate fallback") }
        print("\(checks) update network checks passed; all traffic stubbed; no installation")
    }
}
