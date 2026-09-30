import Foundation

// Compile the production automation extension against in-memory collaborators.
// These tests must never launch the GUI, contact its socket, or change Mac power.
enum HardwareReading {
    static func current() -> SafetyReading {
        SafetyReading(batteryPercent: 80, onAC: true, lidClosed: false,
                      hasExternalDisplay: false, heat: .normal)
    }
}

@MainActor
final class AppModel {
    var active = false
    var busy = false
    var recoveryRequired = false
    var serviceReady = true
    var needsApproval = false
    var standardModeAvailable = false
    var sessionMode = "off"
    var lidEngaged = false
    var waitingForLid: Bool { active && sessionMode == "closedLid" && !lidEngaged }
    var lidClosedSupported = false
    var sessionNotice: String? = nil
    var error: String?
    var monitorPreference = true
    var monitorOn: Bool { active && monitorPreference }
    var starts = 0
    var stops = 0
    var monitorChanges = 0
    var startFailure: String?
    var stopFailure: String?
    var monitorFailure: String?

    func refreshService() {}
    func toggleSession(completion: (() -> Void)? = nil) {
        starts += 1
        error = startFailure
        if startFailure == nil { active = true }
        completion?()
    }
    func stop(completion: ((Bool) -> Void)? = nil) {
        stops += 1
        error = stopFailure
        if stopFailure == nil { active = false; recoveryRequired = false }
        completion?(stopFailure == nil)
    }
    func setMonitor(_ value: Bool) {
        monitorChanges += 1
        if let monitorFailure { error = monitorFailure }
        else { monitorPreference = value }
    }

    func request(_ operation: String, _ enabled: Bool) -> [String: Any] {
        var reply: [String: Any]?
        handleAutomation(["operation": operation, "enabled": enabled]) { reply = $0 }
        guard let reply else { fatalError("Expected exactly one synchronous stub response") }
        return reply
    }
}

var checks = 0
func check(_ condition: Bool, _ message: String) {
    guard condition else { print("FAIL \(message)"); exit(1) }
    checks += 1
    print("PASS \(message)")
}

MainActor.assumeIsolated {
    let inactive = AppModel()
    let monitorOff = inactive.request("set_monitor", false)
    check(monitorOff["code"] as? String == "session_off" && inactive.monitorChanges == 0,
          "inactive Monitor OFF is rejected without display changes")
    check(inactive.request("set_monitor", true)["code"] as? String == "session_off",
          "inactive Monitor ON is rejected")

    let busy = AppModel()
    busy.busy = true
    busy.active = true
    check(busy.request("set_session", false)["code"] as? String == "busy" && busy.stops == 0,
          "busy Session mutation never reaches stop")
    check(busy.request("set_monitor", false)["code"] as? String == "busy" && busy.monitorChanges == 0,
          "busy Monitor mutation never reaches display")

    let recovering = AppModel()
    recovering.recoveryRequired = true
    check(recovering.request("set_session", true)["code"] as? String == "recovery_required"
          && recovering.starts == 0 && recovering.stops == 0,
          "recovery blocks ON without accidentally toggling OFF")
    check(recovering.request("set_session", false)["ok"] as? Bool == true && recovering.stops == 1,
          "OFF during recovery attempts restoration")

    let idempotent = AppModel()
    check(idempotent.request("set_session", false)["ok"] as? Bool == true && idempotent.stops == 0,
          "already OFF Session is a no-op")
    idempotent.active = true
    check(idempotent.request("set_session", true)["ok"] as? Bool == true && idempotent.starts == 0,
          "already ON Session is a no-op")
    check(idempotent.request("set_monitor", true)["ok"] as? Bool == true && idempotent.monitorChanges == 0,
          "equal Monitor ON does not trigger display wake")
    idempotent.monitorPreference = false
    check(idempotent.request("set_monitor", false)["ok"] as? Bool == true && idempotent.monitorChanges == 0,
          "equal Monitor OFF does not schedule physical display sleep")

    let setup = AppModel()
    setup.serviceReady = false
    check(setup.request("set_session", true)["code"] as? String == "setup_required" && setup.starts == 0,
          "missing helper setup cannot start Session")
    let failed = AppModel()
    failed.startFailure = "helper unavailable"
    let failedReply = failed.request("set_session", true)
    check(failedReply["ok"] as? Bool == false && failedReply["code"] as? String == "session_start_failed"
          && failedReply["message"] as? String == "helper unavailable"
          && failedReply["sessionOn"] as? Bool == false,
          "helper failure propagates with actual inactive state")
    let unsupported = AppModel()
    unsupported.serviceReady = false
    unsupported.standardModeAvailable = true
    let unsupportedReply = unsupported.request("set_session", true)
    check(unsupportedReply["code"] as? String == "setup_required" && unsupported.starts == 0,
          "open-lid fallback cannot substitute for the required helper")
    check(unsupportedReply["sessionOn"] as? Bool == false,
          "missing lid support never reports an armed session")
    unsupported.recoveryRequired = true
    check(unsupported.request("set_session", true)["code"] as? String == "recovery_required" && unsupported.starts == 0,
          "missing helper never bypasses recovery guard")
    failed.active = true
    failed.stopFailure = "restore failed"
    check(failed.request("set_session", false)["code"] as? String == "session_stop_failed",
          "failed recovery is not reported as successful OFF")

    let monitor = AppModel()
    monitor.active = true
    monitor.error = "previous unrelated failure"
    check(monitor.request("set_monitor", false)["ok"] as? Bool == true && monitor.error == nil,
          "successful Monitor change clears stale errors")
    monitor.monitorFailure = "display failure"
    check(monitor.request("set_monitor", true)["code"] as? String == "monitor_failed" && !monitor.monitorOn,
          "Monitor failure propagates without changing requested policy")

    let stopped = AppModel()
    stopped.active = true
    let stoppedReply = stopped.request("set_session", false)
    check(stoppedReply["ok"] as? Bool == true && stoppedReply["sessionOn"] as? Bool == false
          && stoppedReply["monitorOn"] as? Bool == false && stopped.monitorChanges == 0,
          "successful Session OFF resets Monitor without requesting physical sleep")
    check(stoppedReply["monitorControllable"] as? Bool == false,
          "Monitor is disabled after Session OFF")
}
print("\(checks) automation guard checks passed")
