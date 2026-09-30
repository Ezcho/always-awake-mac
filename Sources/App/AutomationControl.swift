import Foundation
import CoreFoundation

@MainActor
extension AppModel {
    func automationStatus() -> [String: Any] {
        refreshService()
        let hardware = HardwareReading.current()
        return ["ok": true, "version": AppIdentity.version, "sessionOn": active,
                "monitorOn": monitorOn, "monitorControllable": active && !busy,
                "busy": busy, "recoveryRequired": recoveryRequired,
                "sessionMode": sessionMode, "lidClosedSupported": lidClosedSupported,
                "waitingForLid": waitingForLid, "lidEngaged": lidEngaged,
                "standardModeAvailable": standardModeAvailable,
                "sessionNotice": sessionNotice as Any? ?? NSNull(),
                "serviceRegistered": serviceReady, "needsApproval": needsApproval,
                "lastError": error as Any? ?? NSNull(),
                "safety": ["batteryPercent": hardware.batteryPercent as Any? ?? NSNull(),
                           "onAC": hardware.onAC, "lidClosed": hardware.lidClosed,
                           "hasExternalDisplay": hardware.hasExternalDisplay,
                           "thermalState": String(describing: hardware.heat),
                           "profile": hardware.profile.rawValue,
                           "issue": hardware.issue as Any? ?? NSNull()]]
    }

    func handleAutomation(_ request: [String: Any], completion: @escaping ([String: Any]) -> Void) {
        func fail(_ code: String, _ message: String) {
            var reply = automationStatus()
            reply.merge(ControlWire.failure(code, message)) { _, new in new }
            completion(reply)
        }
        guard let operation = request["operation"] as? String else { fail("invalid_request", "Missing operation"); return }
        if operation == "status" { completion(automationStatus()); return }
        guard operation == "set_session" || operation == "set_monitor",
              Set(request.keys) == Set(["operation", "enabled"]),
              let number = request["enabled"] as? NSNumber,
              CFGetTypeID(number) == CFBooleanGetTypeID() else {
            fail("invalid_request", "Expected set_session or set_monitor and a boolean enabled"); return
        }
        let enabled = number.boolValue
        guard !busy else { fail("busy", "Another operation is in progress; query status before retrying"); return }
        if operation == "set_monitor" {
            guard active else { fail("session_off", "Monitor can only be changed while Session is ON"); return }
            if monitorOn != enabled {
                error = nil
                setMonitor(enabled)
                if let error { fail("monitor_failed", error); return }
            }
            var reply = automationStatus()
            reply["displayPolicy"] = waitingForLid ? "on_lid_close" : (enabled ? "keep_awake" : "sleep_requested")
            completion(reply)
            return
        }
        if enabled {
            guard !recoveryRequired else { fail("recovery_required", "Turn Session OFF to recover before starting"); return }
            if active { completion(automationStatus()); return }
            refreshService()
            guard serviceReady else {
                fail("setup_required", "Install the pika helper package and open pika before enabling a closed-lid session"); return
            }
            toggleSession {
                if self.active && self.error == nil { completion(self.automationStatus()) }
                else { fail("session_start_failed", self.error ?? "Session did not start") }
            }
        } else {
            if !active && !recoveryRequired { completion(automationStatus()); return }
            stop { success in
                if success { completion(self.automationStatus()) }
                else { fail("session_stop_failed", self.error ?? "Sleep setting recovery failed") }
            }
        }
    }
}
