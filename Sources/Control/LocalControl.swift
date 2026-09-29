import Foundation
import Darwin

// Local, per-user IPC only. Never expose this power-control interface on TCP.
enum ControlWire {
    static let directory = "/tmp/pika-control-\(getuid())"
    static let path = directory + "/control.sock"
    static let limit = 65_536

    static func failure(_ code: String, _ message: String) -> [String: Any] {
        ["ok": false, "code": code, "message": message]
    }

    static func address() -> sockaddr_un {
        var addr = sockaddr_un()
        addr.sun_family = sa_family_t(AF_UNIX)
        addr.sun_len = UInt8(MemoryLayout<sockaddr_un>.size)
        withUnsafeMutableBytes(of: &addr.sun_path) { bytes in
            bytes.copyBytes(from: path.utf8CString.map { UInt8(bitPattern: $0) })
        }
        return addr
    }

    static func configure(_ fd: Int32) {
        var timeout = timeval(tv_sec: 20, tv_usec: 0)
        setsockopt(fd, SOL_SOCKET, SO_RCVTIMEO, &timeout, socklen_t(MemoryLayout<timeval>.size))
        setsockopt(fd, SOL_SOCKET, SO_SNDTIMEO, &timeout, socklen_t(MemoryLayout<timeval>.size))
        var one: Int32 = 1
        setsockopt(fd, SOL_SOCKET, SO_NOSIGPIPE, &one, socklen_t(MemoryLayout<Int32>.size))
    }

    static func readLine(_ fd: Int32) throws -> Data? {
        var data = Data()
        var byte: UInt8 = 0
        while data.count <= limit {
            let count = Darwin.read(fd, &byte, 1)
            if count == 0 { return data.isEmpty ? nil : data }
            if count < 0 {
                if errno == EINTR { continue }
                throw NSError(domain: NSPOSIXErrorDomain, code: Int(errno))
            }
            if byte == 10 { return data }
            data.append(byte)
        }
        throw NSError(domain: "pika", code: 1, userInfo: [NSLocalizedDescriptionKey: "Message exceeds 64 KiB"])
    }

    static func write(_ data: Data, to fd: Int32) throws {
        var framed = data
        framed.append(10)
        try framed.withUnsafeBytes { bytes in
            var offset = 0
            while offset < bytes.count {
                let sent = Darwin.write(fd, bytes.baseAddress!.advanced(by: offset), bytes.count - offset)
                if sent < 0 && errno == EINTR { continue }
                guard sent > 0 else { throw NSError(domain: NSPOSIXErrorDomain, code: Int(errno)) }
                offset += sent
            }
        }
    }

    static func call(_ request: [String: Any]) -> [String: Any] {
        let fd = socket(AF_UNIX, SOCK_STREAM, 0)
        guard fd >= 0 else { return failure("connection_failed", "Could not create local socket") }
        defer { close(fd) }
        configure(fd)
        var addr = address()
        let connected = withUnsafePointer(to: &addr) {
            $0.withMemoryRebound(to: sockaddr.self, capacity: 1) { connect(fd, $0, socklen_t(MemoryLayout<sockaddr_un>.size)) }
        }
        guard connected == 0 else {
            return failure("app_not_running", "Open the MCP-enabled pika.app on this Mac, then retry.")
        }
        var uid: uid_t = 0; var gid: gid_t = 0
        guard getpeereid(fd, &uid, &gid) == 0, uid == getuid() else {
            return failure("unauthorized_peer", "Local app must belong to the current user")
        }
        do {
            try write(JSONSerialization.data(withJSONObject: request), to: fd)
            guard let data = try readLine(fd), let reply = try JSONSerialization.jsonObject(with: data) as? [String: Any] else {
                return failure("invalid_response", "No valid response from pika")
            }
            return reply
        } catch {
            return failure("connection_failed", "App response failed or timed out. Check pika_status before retrying: \(error.localizedDescription)")
        }
    }
}

final class LocalControlServer {
    private var listener: Int32 = -1
    private var lock: Int32 = -1
    private let connections = DispatchSemaphore(value: 8)

    func start(handler: @escaping ([String: Any], @escaping ([String: Any]) -> Void) -> Void) throws {
        if mkdir(ControlWire.directory, 0o700) != 0 && errno != EEXIST { throw posixError() }
        var info = stat()
        guard lstat(ControlWire.directory, &info) == 0,
              info.st_uid == getuid(), info.st_mode & S_IFMT == S_IFDIR,
              info.st_mode & 0o777 == 0o700 else {
            throw NSError(domain: "pika", code: 2, userInfo: [NSLocalizedDescriptionKey: "Unsafe local control directory"])
        }
        lock = Darwin.open(ControlWire.directory + "/lock", O_CREAT | O_RDWR | O_NOFOLLOW | O_CLOEXEC, 0o600)
        guard lock >= 0, flock(lock, LOCK_EX | LOCK_NB) == 0 else { throw posixError() }
        // The exclusive lock prevents a second app from removing a live endpoint.
        if lstat(ControlWire.path, &info) == 0 {
            guard info.st_uid == getuid(), info.st_mode & S_IFMT == S_IFSOCK else {
                throw NSError(domain: "pika", code: 3, userInfo: [NSLocalizedDescriptionKey: "Unexpected local control file"])
            }
            guard unlink(ControlWire.path) == 0 else { throw posixError() }
        } else if errno != ENOENT { throw posixError() }
        listener = socket(AF_UNIX, SOCK_STREAM, 0)
        guard listener >= 0 else { throw posixError() }
        _ = fcntl(listener, F_SETFD, FD_CLOEXEC)
        var addr = ControlWire.address()
        let bound = withUnsafePointer(to: &addr) {
            $0.withMemoryRebound(to: sockaddr.self, capacity: 1) { bind(listener, $0, socklen_t(MemoryLayout<sockaddr_un>.size)) }
        }
        guard bound == 0, chmod(ControlWire.path, 0o600) == 0, listen(listener, 8) == 0 else { throw posixError() }
        DispatchQueue(label: "pika.local-control").async { [self] in
            while true {
                let fd = accept(listener, nil, nil)
                if fd < 0 { if errno == EINTR { continue }; break }
                guard connections.wait(timeout: .now()) == .success else { close(fd); continue }
                _ = fcntl(fd, F_SETFD, FD_CLOEXEC)
                DispatchQueue.global(qos: .userInitiated).async { [self] in
                    defer { close(fd); connections.signal() }
                    serve(fd, handler: handler)
                }
            }
        }
    }

    private func serve(_ fd: Int32, handler: @escaping ([String: Any], @escaping ([String: Any]) -> Void) -> Void) {
        ControlWire.configure(fd)
        // Do not execute a request that sat behind a blocked UI or slow sender.
        // Helper calls time out after 12s; leave room inside the client's 20s timeout.
        let deadline = Date().addingTimeInterval(2)
        var uid: uid_t = 0; var gid: gid_t = 0
        guard getpeereid(fd, &uid, &gid) == 0, uid == getuid() else { return }
        do {
            guard let data = try ControlWire.readLine(fd),
                  let request = try JSONSerialization.jsonObject(with: data) as? [String: Any] else { return }
            let semaphore = DispatchSemaphore(value: 0)
            let resultLock = NSLock()
            var response = ControlWire.failure("timeout", "App is busy; query status before retrying")
            DispatchQueue.main.async {
                guard Date() < deadline else { semaphore.signal(); return }
                handler(request) { value in
                    resultLock.lock(); response = value; resultLock.unlock()
                    semaphore.signal()
                }
            }
            _ = semaphore.wait(timeout: .now() + 16)
            resultLock.lock(); let result = response; resultLock.unlock()
            try ControlWire.write(JSONSerialization.data(withJSONObject: result), to: fd)
        } catch { /* A malformed or disconnected client cannot affect the app session. */ }
    }

    private func posixError() -> NSError { NSError(domain: NSPOSIXErrorDomain, code: Int(errno)) }
    deinit { if listener >= 0 { close(listener) }; if lock >= 0 { close(lock) } }
}
