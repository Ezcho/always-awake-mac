import Foundation
import CoreFoundation

final class MCPServer {
    private var initialized = false
    private let control: ([String: Any]) -> [String: Any]
    init(control: @escaping ([String: Any]) -> [String: Any] = ControlWire.call) { self.control = control }

    static let tools: [[String: Any]] = [
        tool("pika_status", "Read pika session, requested monitor policy, helper registration, battery and thermal status. Registration does not prove helper connectivity.", readOnly: true),
        tool("pika_set_session", "Set Session ON/OFF in the running pika menu-bar app. Safety checks remain active. OFF releases sleep prevention and resets Monitor to OFF without immediately sleeping the display. Closed-lid operation requires a ready privileged helper; there is no open-lid fallback. ON does not blank or wake the screen. In closed-lid mode display policy waits for lid closure; inspect waitingForLid and lidEngaged as well as sessionMode and lidClosedSupported.", readOnly: false),
        tool("pika_set_monitor", "Set the monitor policy while Session is ON. In closed-lid mode this only saves a preference while waitingForLid; closing the lid applies it. Once applied, true keeps/wakes the display; false requests display sleep after 3 seconds. Reports the requested policy, not physical screen state.", readOnly: false)
    ]

    private static func tool(_ name: String, _ description: String, readOnly: Bool) -> [String: Any] {
        ["name": name, "description": description,
         "inputSchema": ["type": "object", "properties": readOnly ? [:] : ["enabled": ["type": "boolean"]],
                         "required": readOnly ? [] : ["enabled"], "additionalProperties": false],
         "annotations": ["readOnlyHint": readOnly, "destructiveHint": !readOnly,
                         "idempotentHint": true, "openWorldHint": false]]
    }

    func handle(_ data: Data) -> [String: Any]? {
        guard let value = try? JSONSerialization.jsonObject(with: data) else { return error(NSNull(), -32700, "Parse error") }
        guard let message = value as? [String: Any], message["jsonrpc"] as? String == "2.0",
              let method = message["method"] as? String else { return error(NSNull(), -32600, "Invalid request") }
        // JSON-RPC notifications, including initialized/cancelled, never get responses.
        guard let id = message["id"] else { return nil }
        guard id is String || ((id as? NSNumber).map { CFGetTypeID($0) != CFBooleanGetTypeID() } ?? false) else {
            return error(NSNull(), -32600, "Invalid request id")
        }
        let params = message["params"] as? [String: Any] ?? [:]
        if method == "initialize" {
            guard !initialized else { return error(id, -32600, "Already initialized") }
            guard let version = params["protocolVersion"] as? String,
                  params["capabilities"] is [String: Any], params["clientInfo"] is [String: Any] else {
                return error(id, -32602, "Invalid initialize parameters")
            }
            initialized = true
            let supported = ["2024-11-05", "2025-03-26", "2025-06-18", "2025-11-25"]
            return result(id, ["protocolVersion": supported.contains(version) ? version : "2025-11-25",
                               "capabilities": ["tools": ["listChanged": false]],
                               "serverInfo": ["name": "pika", "version": AppIdentity.version],
                               "instructions": "Controls the local running pika app. Use explicit enabled values. Inspect tool errors and recoveryRequired; never assume a session started. Safety protections cannot be disabled through MCP."])
        }
        if method == "ping" { return result(id, [:]) }
        guard initialized else { return error(id, -32002, "Initialize first") }
        if method == "tools/list" { return result(id, ["tools": Self.tools]) }
        guard method == "tools/call" else { return error(id, -32601, "Method not found") }
        guard let name = params["name"] as? String, Self.tools.contains(where: { $0["name"] as? String == name }) else {
            return error(id, -32602, "Unknown tool")
        }
        if let raw = params["arguments"], !(raw is [String: Any]) { return error(id, -32602, "Arguments must be an object") }
        let arguments = params["arguments"] as? [String: Any] ?? [:]
        var request: [String: Any]
        if name == "pika_status" {
            guard arguments.isEmpty else { return error(id, -32602, "Status takes no arguments") }
            request = ["operation": "status"]
        } else {
            guard arguments.count == 1, let enabled = arguments["enabled"] as? NSNumber,
                  CFGetTypeID(enabled) == CFBooleanGetTypeID() else {
                return error(id, -32602, "enabled must be a boolean")
            }
            request = ["operation": name == "pika_set_session" ? "set_session" : "set_monitor", "enabled": enabled.boolValue]
        }
        let reply = control(request)
        let text = String(data: (try? JSONSerialization.data(withJSONObject: reply, options: [.sortedKeys])) ?? Data(), encoding: .utf8) ?? "{}"
        return result(id, ["content": [["type": "text", "text": text]], "structuredContent": reply, "isError": !(reply["ok"] as? Bool ?? false)])
    }

    private func result(_ id: Any, _ result: [String: Any]) -> [String: Any] { ["jsonrpc": "2.0", "id": id, "result": result] }
    private func error(_ id: Any, _ code: Int, _ message: String) -> [String: Any] {
        ["jsonrpc": "2.0", "id": id, "error": ["code": code, "message": message]]
    }
}
