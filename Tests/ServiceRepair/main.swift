import Foundation
import Darwin

var checks = 0
func check(_ value: Bool, _ message: String) {
    guard value else { fatalError("FAIL: \(message)") }
    checks += 1
    print("PASS: \(message)")
}
func accepted(_ reply: [String: Any]) -> Bool {
    do { try ServiceRepairPolicy.requireIdleApplication(reply); return true }
    catch { return false }
}

let idle: [String: Any] = ["ok": true, "sessionOn": false, "recoveryRequired": false, "busy": false]
check(accepted(idle), "a fully confirmed idle app allows legacy maintenance")
for key in ["sessionOn", "recoveryRequired", "busy"] {
    var reply = idle
    reply[key] = true
    check(!accepted(reply), "\(key) prevents legacy maintenance")
    reply.removeValue(forKey: key)
    check(!accepted(reply), "missing \(key) fails closed")
}
for code in [ENOENT, ECONNREFUSED] {
    let reply = ControlWire.connectionFailure(code)
    check(reply["code"] as? String == "app_not_running" && accepted(reply),
          "absent endpoint error \(code) allows legacy maintenance")
}
for code in [EACCES, EPERM, EMFILE, ENOBUFS, EAGAIN] {
    let reply = ControlWire.connectionFailure(code)
    check(reply["code"] as? String == "connection_failed" && !accepted(reply),
          "ambiguous connection error \(code) prevents legacy maintenance")
}
for reply in [[:], ["ok": false], ["ok": false, "code": "timeout"],
              ["ok": false, "code": "invalid_response"], ["ok": false, "code": "unauthorized_peer"]] as [[String: Any]] {
    check(!accepted(reply), "unknown, malformed, or untrusted status fails closed")
}
do {
    try ServiceRepairPolicy.requireLegacyRepair(installedHelperPresent: false)
    check(true, "legacy repair is available without an installed PKG helper")
} catch { fatalError("Unexpected legacy repair rejection") }
do {
    try ServiceRepairPolicy.requireLegacyRepair(installedHelperPresent: true)
    fatalError("PKG helper must block legacy registration")
} catch { check(true, "PKG helper prevents competing legacy registration") }
print("\(checks) service repair checks passed")
