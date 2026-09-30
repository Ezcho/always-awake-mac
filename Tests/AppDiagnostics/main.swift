import Foundation

// Compile the real AppModel against inert collaborators. Never call launchd,
// create a Session, access the app's IPC socket, or change display/power settings.
enum Signature { static func isAdHoc(_ url: URL) -> Bool { true } }
enum InstalledHelper {
    static var isPresent: Bool { true }
    static var invalid = false
    static func validateForClient() throws {
        if invalid { throw AwakeError("installed helper no longer matches") }
    }
}
enum HardwareReading {
    static var issue: String?
    struct Reading { var issue: String? { HardwareReading.issue } }
    static func current() -> Reading { Reading() }
    static func lidIsClosed() -> Bool? { false }
}
final class DisplayController {
    var onError: ((String) -> Void)?
    func arm() {}
    func disarm() {}
    func release() {}
    func apply(keepOn: Bool) throws {}
}
@MainActor
final class HelperClient {
    enum Operation { case start, stop, heartbeat, status }
    var onDisconnect: (() -> Void)?
    var next: Result<ServiceReply, Error> = .success(ServiceReply())
    func call(_ operation: Operation, completion: @escaping (Result<ServiceReply, Error>) -> Void) {
        completion(next)
    }
    func invalidate() {}
}
enum SystemSleepController { static func requireSystemSleepEnabled() throws {} }
enum HelperSetupDownload {
    static func download() async throws -> URL { throw AwakeError("Download is unavailable in this test") }
}

var checks = 0
func check(_ value: Bool, _ message: String) {
    guard value else { fatalError("FAIL: \(message)") }
    checks += 1
    print("PASS: \(message)")
}

MainActor.assumeIsolated {
    let model = AppModel()
    model.checkHelperConnection()
    check(model.setupStatus == "보조 서비스 연결 완료" && model.helperConnected,
          "successful status sets the setup connection message")
    model.client.onDisconnect?()
    check(model.setupStatus == nil && !model.helperConnected,
          "disconnect removes a stale connection success message")

    model.checkHelperConnection()
    model.client.next = .failure(AwakeError("current start failure"))
    model.toggleSession()
    check(model.setupStatus == nil && model.error == "current start failure" && !model.active,
          "failed start exposes its new error instead of stale setup success")

    model.client.next = .success(ServiceReply())
    model.checkHelperConnection()
    model.client.next = .failure(AwakeError("current recovery failure"))
    model.stop()
    check(model.setupStatus == nil && model.error == "current recovery failure" && model.recoveryRequired,
          "failed recovery exposes its new error instead of stale setup success")
    model.recoveryRequired = false // Cancel the test model's recovery timer.

    model.client.next = .success(ServiceReply())
    model.checkHelperConnection()
    InstalledHelper.invalid = true
    model.toggleSession()
    check(model.setupStatus == nil && model.error == "installed helper no longer matches",
          "failed service preparation cannot retain stale setup success")

    InstalledHelper.invalid = false
    model.checkHelperConnection()
    InstalledHelper.invalid = true
    model.checkHelperConnection()
    check(model.setupStatus == nil && !model.helperConnected,
          "unavailable helper status clears its earlier connection success")

    InstalledHelper.invalid = false
    model.checkHelperConnection()
    HardwareReading.issue = "battery safety prevents start"
    model.toggleSession()
    check(model.setupStatus == nil && model.error == HardwareReading.issue && !model.active,
          "safety rejection before start cannot retain stale setup success")
}
print("\(checks) app diagnostics checks passed")
