import Foundation

var calls: [[String: Any]] = []
let server = MCPServer { request in
    calls.append(request)
    if request["operation"] as? String == "set_session" {
        return ["ok": false, "code": "session_start_failed", "sessionOn": false, "message": "helper unavailable"]
    }
    return ["ok": true, "sessionOn": false, "monitorOn": false]
}
var count = 0
func check(_ condition: @autoclosure () -> Bool, _ message: String) {
    guard condition() else { print("FAIL \(message)"); exit(1) }
    count += 1; print("PASS \(message)")
}
func rpc(_ method: String, _ params: [String: Any] = [:], id: Any = 1) -> [String: Any] {
    server.handle(try! JSONSerialization.data(withJSONObject: ["jsonrpc": "2.0", "id": id, "method": method, "params": params]))!
}
func code(_ reply: [String: Any]) -> Int? { (reply["error"] as? [String: Any])?["code"] as? Int }
check(code(rpc("tools/list")) == -32002, "tools require initialization")
check(code(rpc("initialize", ["protocolVersion": "2025-11-25"])) == -32602, "reject incomplete initialization")
let initialized = rpc("initialize", ["protocolVersion": "2025-11-25", "capabilities": [:], "clientInfo": ["name": "test", "version": "1"]], id: "init")
check(initialized["id"] as? String == "init", "preserve string request ID")
check((initialized["result"] as? [String: Any])?["protocolVersion"] as? String == "2025-11-25", "negotiate MCP protocol")
let listed = rpc("tools/list")["result"] as! [String: Any]
check((listed["tools"] as! [[String: Any]]).count == 3, "expose three tools")
check(code(rpc("does_not_exist")) == -32601, "unknown method is a JSON-RPC error")
check(code(rpc("tools/call", ["name": "unknown"])) == -32602, "unknown tool rejected")
for invalid: Any in [1, 0, "true", NSNull()] {
    check(code(rpc("tools/call", ["name": "pika_set_session", "arguments": ["enabled": invalid]])) == -32602, "reject nonboolean enabled: \(invalid)")
}
check(calls.isEmpty, "invalid requests never reach control socket")
let status = rpc("tools/call", ["name": "pika_status"])["result"] as! [String: Any]
check(status["isError"] as? Bool == false, "read status returns success")
check(calls.last?["operation"] as? String == "status", "status routed correctly")
let failed = rpc("tools/call", ["name": "pika_set_session", "arguments": ["enabled": true]])["result"] as! [String: Any]
check(failed["isError"] as? Bool == true, "helper failure is a tool error, never success")
check((failed["structuredContent"] as? [String: Any])?["sessionOn"] as? Bool == false, "failure retains real session state")
_ = rpc("tools/call", ["name": "pika_set_monitor", "arguments": ["enabled": false]])
check(calls.last?["operation"] as? String == "set_monitor" && calls.last?["enabled"] as? Bool == false, "monitor OFF is an explicit desired state")
let before = calls.count
let notification = server.handle(Data(#"{"jsonrpc":"2.0","method":"tools/call","params":{"name":"pika_set_session","arguments":{"enabled":true}}}"#.utf8))
check(notification == nil && calls.count == before, "notifications never trigger power operations or responses")
check(code(server.handle(Data("bad-json".utf8))!) == -32700, "malformed JSON rejected")
check(code(server.handle(Data("[]".utf8))!) == -32600, "batches rejected")
check(code(rpc("tools/call", ["name": "pika_status", "arguments": ["extra": true]])) == -32602, "status rejects extra arguments")
check(code(rpc("tools/call", ["name": "pika_set_monitor", "arguments": ["enabled": true, "extra": 1]])) == -32602, "mutation rejects extra arguments")
print("\(count) MCP protocol checks passed")
