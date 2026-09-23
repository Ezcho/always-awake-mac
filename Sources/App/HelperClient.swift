import Foundation

@MainActor
final class HelperClient {
    enum Operation { case start, stop, heartbeat, status }
    private var connection: NSXPCConnection?
    var onDisconnect: (() -> Void)?

    private func connect() throws -> NSXPCConnection {
        if let connection { return connection }
        let helperURL = Bundle.main.bundleURL.appendingPathComponent("Contents/Library/HelperTools/AlwaysAwakeHelper")
        let requirement = try Signature.requirement(for: helperURL)
        let value = NSXPCConnection(machServiceName: AppIdentity.serviceName, options: .privileged)
        value.setCodeSigningRequirement(requirement)
        value.remoteObjectInterface = NSXPCInterface(with: AwakeServiceProtocol.self)
        value.invalidationHandler = { [weak self, weak value] in
            DispatchQueue.main.async {
                guard let self, self.connection === value else { return }
                self.connection = nil
                self.onDisconnect?()
            }
        }
        value.interruptionHandler = { [weak value] in value?.invalidate() }
        value.resume()
        connection = value
        return value
    }

    func call(_ operation: Operation, completion: @escaping (Result<ServiceReply, Error>) -> Void) {
        // XPC can call the error and reply handlers on different queues; resolve on main once.
        var finished = false
        let finish: (Result<ServiceReply, Error>) -> Void = { result in
            DispatchQueue.main.async {
                guard !finished else { return }
                finished = true
                completion(result)
            }
        }
        do {
            let value = try connect()
            guard let proxy = value.remoteObjectProxyWithErrorHandler({ _ in
                finish(.failure(AwakeError("보조 서비스에 연결할 수 없습니다. 시스템 설정에서 Always Awake 허용 여부를 확인해 주세요.")))
            }) as? AwakeServiceProtocol else { throw AwakeError("보조 서비스를 찾을 수 없습니다.") }
            let reply: (Data) -> Void = { data in
                do { finish(.success(try JSONDecoder().decode(ServiceReply.self, from: data))) }
                catch { finish(.failure(AwakeError("보조 서비스 응답을 읽을 수 없습니다."))) }
            }
            switch operation {
            case .start: proxy.beginSession(reply: reply)
            case .stop: proxy.endSession(reply: reply)
            case .heartbeat: proxy.heartbeat(reply: reply)
            case .status: proxy.status(reply: reply)
            }
            DispatchQueue.main.asyncAfter(deadline: .now() + 12) { [weak self, weak value] in
                guard !finished else { return }
                // Drop a timed-out start so its eventual effect cannot become an orphan session.
                if self?.connection === value { value?.invalidate() }
                finish(.failure(AwakeError("보조 서비스 응답이 지연됩니다. 잠자기 설정을 복구하고 있습니다.")))
            }
        } catch { finish(.failure(error)) }
    }

    func invalidate() { connection?.invalidate(); connection = nil }
}
