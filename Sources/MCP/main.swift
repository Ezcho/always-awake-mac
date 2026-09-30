import Foundation
import Darwin

// MCP stdio is newline-delimited JSON only; diagnostics never go to stdout.
signal(SIGPIPE, SIG_IGN)
let server = MCPServer()
do {
    while try autoreleasepool(invoking: { () throws -> Bool in
        // A stdio server has no AppKit run loop to drain Foundation's temporary
        // objects. Bound their lifetime to one request, including encoding.
        guard let line = try ControlWire.readLine(STDIN_FILENO) else { return false }
        if let reply = server.handle(line) {
            try ControlWire.write(JSONSerialization.data(withJSONObject: reply, options: [.sortedKeys]), to: STDOUT_FILENO)
        }
        return true
    }) {}
} catch {
    FileHandle.standardError.write(Data("pika MCP: \(error.localizedDescription)\n".utf8))
    exit(1)
}
