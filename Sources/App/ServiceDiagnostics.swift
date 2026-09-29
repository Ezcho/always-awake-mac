import Foundation
import ServiceManagement

/// Explicit command-line diagnostics through the same signed XPC client as the UI.
/// --check-service is read-only; --test-session starts and immediately ends a session.
@MainActor
enum ServiceDiagnostics {
    // Use after replacing an ad-hoc signed build, whose pinned signature changes.
    static func repairRegistration() {
        Task { @MainActor in
            let service = SMAppService.daemon(plistName: AppIdentity.helperPlist)
            do {
                if service.status != .notRegistered && service.status != .notFound {
                    try await service.unregister()
                }
                try service.register()
                print("Service registration status: \(service.status.rawValue)")
                exit(service.status == .enabled ? 0 : 1)
            } catch {
                print("Service registration status: \(service.status.rawValue), \(error.localizedDescription)")
                exit(1)
            }
        }
    }

    static func run(testSession: Bool) {
        let client = HelperClient()
        func finish(_ success: Bool, _ message: String) {
            print(message)
            client.invalidate()
            exit(success ? 0 : 1)
        }
        DispatchQueue.main.asyncAfter(deadline: .now() + 30) {
            finish(false, "FAIL: service diagnostic timed out; connection released")
        }
        client.call(.status) { result in
            guard case .success(let status) = result else {
                if case .failure(let error) = result { finish(false, "FAIL: \(error.localizedDescription)") }
                return
            }
            guard testSession else {
                finish(true, "PASS: service connected, active=\(status.active), recoveryRequired=\(status.recoveryRequired)")
                return
            }
            guard !status.active && !status.recoveryRequired else {
                finish(false, "FAIL: existing session or recovery pending; left unchanged")
                return
            }
            client.call(.start) { result in
                guard case .success(let started) = result, started.active, started.ownedByCaller else {
                    let message: String
                    switch result {
                    case .success(let reply): message = reply.message ?? "session did not start"
                    case .failure(let error): message = error.localizedDescription
                    }
                    finish(false, "FAIL: \(message)")
                    return
                }
                print("PASS: session ON, owned by diagnostic client")
                client.call(.stop) { result in
                    guard case .success(let stopped) = result, !stopped.active, !stopped.recoveryRequired else {
                        finish(false, "FAIL: session OFF not confirmed; connection released for recovery")
                        return
                    }
                    finish(true, "PASS: session OFF, original sleep setting restored")
                }
            }
        }
    }
}
