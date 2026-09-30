import Foundation
import ServiceManagement

/// Explicit command-line diagnostics through the same signed XPC client as the UI.
/// --check-service is read-only; --test-session starts and immediately ends a session.
@MainActor
enum ServiceDiagnostics {
    // Installer migration only. Never unregister while the persistent sleep
    // override is active; the old helper must restore it first.
    static func unregisterLegacyService() {
        Task { @MainActor in
            do {
                try requireIdleLegacyService()
                let service = SMAppService.daemon(plistName: AppIdentity.helperPlist)
                if service.status != .notRegistered && service.status != .notFound {
                    try await service.unregister()
                    try await Task.sleep(nanoseconds: 2_000_000_000)
                }
                guard service.status == .notRegistered || service.status == .notFound else {
                    throw AwakeError("기존 보조 서비스 등록 해제가 확인되지 않았습니다.")
                }
                try SystemSleepController.requireSystemSleepEnabled()
                print("PASS: legacy helper unregistered; system sleep remains enabled")
                exit(0)
            } catch {
                print("FAIL: \(error.localizedDescription)")
                exit(1)
            }
        }
    }

    private static func requireIdleLegacyService() throws {
        try SystemSleepController.requireSystemSleepEnabled()
        try ServiceRepairPolicy.requireIdleApplication(ControlWire.call(["operation": "status"]))
        // The socket query can take time; recheck immediately before mutation.
        try SystemSleepController.requireSystemSleepEnabled()
    }

    // Legacy app-managed services only. PKG installations have a different owner.
    static func repairRegistration() {
        Task { @MainActor in
            let service = SMAppService.daemon(plistName: AppIdentity.helperPlist)
            do {
                try ServiceRepairPolicy.requireLegacyRepair(installedHelperPresent: InstalledHelper.isPresent)
                try requireIdleLegacyService()
                if service.status != .notRegistered && service.status != .notFound {
                    try await service.unregister()
                    // macOS may finish the callback before smd finishes removing the job.
                    try await Task.sleep(nanoseconds: 2_000_000_000)
                }
                guard service.status == .notRegistered || service.status == .notFound else {
                    throw AwakeError("기존 보조 서비스 등록 해제가 확인되지 않았습니다.")
                }
                try ServiceRepairPolicy.requireLegacyRepair(installedHelperPresent: InstalledHelper.isPresent)
                try requireIdleLegacyService()
                try service.register()
                print("Service registration status: \(service.status.rawValue)")
                guard service.status == .enabled else { exit(1) }
                // Enabled is an approval state, not proof that launchd can run the helper.
                run(testSession: false)
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
