import Foundation
import Darwin

final class ServiceDelegate: NSObject, NSXPCListenerDelegate {
    let queue = DispatchQueue(label: "com.alwaysawake.power")
    let engine: SessionEngine
    let clientRequirement: String
    var ownerUID: uid_t?
    private var safetySleepPending = false
    private var timer: DispatchSourceTimer?
    private var signals: [DispatchSourceSignal] = []

    init(configuration: Void) throws {
        // Recover first, even if an interrupted update left the GUI signature invalid.
        engine = SessionEngine(driver: SystemSleepDriver(), journal: try DiskRecoveryJournal())
        // The helper lives at App/Contents/Library/HelperTools/AlwaysAwakeHelper.
        let appURL = try HelperInstallation.appURL()
        clientRequirement = try Signature.requirement(for: appURL)
        super.init()
        let watchdog = DispatchSource.makeTimerSource(queue: queue)
        watchdog.schedule(deadline: .now() + 5, repeating: 5)
        watchdog.setEventHandler { [weak self] in
            guard let self else { return }
            let wasActive = self.engine.owner != nil
            let thermalOrBatteryIssue = wasActive ? HardwareReading.current().issue : nil
            if wasActive && thermalOrBatteryIssue != nil { self.safetySleepPending = true }
            let userChanged = self.ownerUID != nil && PowerSafety.consoleUser() != self.ownerUID
            self.engine.tick(safetyIssue: userChanged ? "사용자가 전환되어 세션을 종료했습니다." : thermalOrBatteryIssue)
            if self.safetySleepPending && self.engine.owner == nil && !self.engine.recoveryRequired {
                self.safetySleepPending = false
                PowerSafety.sleepNow()
            }
            if self.engine.owner == nil { self.ownerUID = nil }
        }
        watchdog.resume()
        timer = watchdog
        for sig in [SIGTERM, SIGINT] {
            signal(sig, SIG_IGN)
            let source = DispatchSource.makeSignalSource(signal: sig, queue: queue)
            source.setEventHandler { [weak self] in
                do { try self?.engine.shutdown(); exit(0) }
                catch { NSLog("Always Awake recovery pending: %@", error.localizedDescription); exit(1) }
            }
            source.resume()
            signals.append(source)
        }
    }

    func listener(_ listener: NSXPCListener, shouldAcceptNewConnection connection: NSXPCConnection) -> Bool {
        guard connection.effectiveUserIdentifier == PowerSafety.consoleUser() else { return false }
        connection.setCodeSigningRequirement(clientRequirement)
        let client = ServiceClient(delegate: self, uid: connection.effectiveUserIdentifier)
        connection.exportedInterface = NSXPCInterface(with: AwakeServiceProtocol.self)
        connection.exportedObject = client
        let cleanup = { [weak self] in
            guard let self else { return }
            self.queue.async {
                self.engine.disconnected(owner: client.id)
                if self.engine.owner == nil { self.ownerUID = nil }
            }
        }
        connection.invalidationHandler = cleanup
        connection.interruptionHandler = cleanup
        connection.resume()
        return true
    }
}

final class ServiceClient: NSObject, AwakeServiceProtocol {
    let id = UUID()
    let uid: uid_t
    unowned let delegate: ServiceDelegate
    init(delegate: ServiceDelegate, uid: uid_t) { self.delegate = delegate; self.uid = uid }

    private func perform(_ operation: @escaping () throws -> Void, reply: @escaping (Data) -> Void) {
        delegate.queue.async {
            do {
                guard PowerSafety.consoleUser() == self.uid else { throw AwakeError("현재 로그인한 사용자만 조작할 수 있습니다.") }
                try operation()
                reply(self.delegate.engine.reply(for: self.id).data)
            } catch { reply(self.delegate.engine.reply(for: self.id, error: error).data) }
        }
    }

    func beginSession(reply: @escaping (Data) -> Void) {
        perform({
            try self.delegate.engine.begin(owner: self.id, safetyIssue: PowerSafety.issue(ownerUID: self.uid))
            self.delegate.ownerUID = self.uid
        }, reply: reply)
    }
    func endSession(reply: @escaping (Data) -> Void) {
        perform({
            try self.delegate.engine.end(owner: self.id)
            self.delegate.ownerUID = nil
        }, reply: reply)
    }
    func heartbeat(reply: @escaping (Data) -> Void) {
        perform({
            // The watchdog owns safety transitions, including system sleep. A heartbeat
            // must not consume that transition before the watchdog gets to run.
            try self.delegate.engine.renew(owner: self.id, safetyIssue: nil)
        }, reply: reply)
    }
    func status(reply: @escaping (Data) -> Void) { perform({}, reply: reply) }
}

// Read-only installation check: no journal, listener or power settings are touched.
if CommandLine.arguments.dropFirst().contains("--check-installation") {
    do {
        let app = try HelperInstallation.appURL()
        _ = try Signature.requirement(for: app)
        print("Installation verified: \(app.path)")
        exit(0)
    } catch { fputs("\(error.localizedDescription)\n", stderr); exit(1) }
}

guard geteuid() == 0 else { fputs("AlwaysAwakeHelper must be launched by macOS as a system service.\n", stderr); exit(1) }
do {
    let delegate = try ServiceDelegate(configuration: ())
    let listener = NSXPCListener(machServiceName: AppIdentity.serviceName)
    listener.delegate = delegate
    listener.resume()
    withExtendedLifetime(delegate) { dispatchMain() }
} catch {
    NSLog("Always Awake helper: %@", error.localizedDescription)
    exit(1)
}
