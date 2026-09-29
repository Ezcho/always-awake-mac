import Foundation
import Darwin

// MCP stdio is newline-delimited JSON only; diagnostics never go to stdout.
signal(SIGPIPE, SIG_IGN)
let server = MCPServer()
do {
    while let line = try ControlWire.readLine(STDIN_FILENO) {
        if let reply = server.handle(line) {
            try ControlWire.write(JSONSerialization.data(withJSONObject: reply, options: [.sortedKeys]), to: STDOUT_FILENO)
        }
    }
} catch {
    FileHandle.standardError.write(Data("pika MCP: \(error.localizedDescription)\n".utf8))
    exit(1)
}
