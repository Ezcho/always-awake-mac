import Foundation
import Darwin

// MCP stdio is newline-delimited JSON only; diagnostics never go to stdout.
signal(SIGPIPE, SIG_IGN)
// A client can die while another inherited pipe writer prevents stdin EOF.
// Watch that client directly without polling or disturbing other live clients.
let clientPID = getppid()
guard clientPID > 1 else { exit(0) }
let clientExit = DispatchSource.makeProcessSource(identifier: clientPID, eventMask: .exit, queue: .global(qos: .utility))
clientExit.setEventHandler { exit(0) }
clientExit.resume()
// Close the race between capturing the parent and registering the exit source.
guard getppid() == clientPID else { exit(0) }
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
