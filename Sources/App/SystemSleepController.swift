import Foundation
import IOKit.pwr_mgt

// Unprivileged idle-sleep prevention. macOS retains lid/manual/low-battery sleep.
final class SystemSleepController {
    private var assertion: IOPMAssertionID = 0

    func start() throws {
        guard assertion == 0 else { return }
        try Self.requireSystemSleepEnabled()
        let result = IOPMAssertionCreateWithName(kIOPMAssertionTypePreventUserIdleSystemSleep as CFString,
            IOPMAssertionLevel(kIOPMAssertionLevelOn), "pika · Standard session" as CFString, &assertion)
        guard result == kIOReturnSuccess else {
            assertion = 0
            throw AwakeError("일반 잠자기 방지를 시작하지 못했습니다 (\(result)).")
        }
    }

    static func requireSystemSleepEnabled() throws {
        // A stale privileged override would defeat this mode's safety stop.
        let process = Process()
        process.executableURL = URL(fileURLWithPath: "/usr/bin/pmset")
        process.arguments = ["-g"]
        process.environment = ["PATH": "/usr/bin:/bin:/usr/sbin:/sbin", "LANG": "C"]
        let output = Pipe()
        process.standardOutput = output
        process.standardError = output
        let done = DispatchSemaphore(value: 0)
        process.terminationHandler = { _ in done.signal() }
        try process.run()
        guard done.wait(timeout: .now() + 3) == .success else {
            process.terminate()
            throw AwakeError("잠자기 설정 확인 시간이 초과되었습니다. 다시 시도해 주세요.")
        }
        let text = String(decoding: output.fileHandleForReading.readDataToEndOfFile(), as: UTF8.self)
        let disabled = text.split(separator: "\n").compactMap { line -> Bool? in
            let parts = line.split(whereSeparator: { $0.isWhitespace })
            guard parts.count == 2, parts[0] == "SleepDisabled", ["0", "1"].contains(parts[1]) else { return nil }
            return parts[1] == "1"
        }.first
        guard process.terminationStatus == 0, let disabled else {
            throw AwakeError("현재 잠자기 설정을 확인할 수 없어 세션을 시작하지 않았습니다.")
        }
        guard !disabled else {
            throw AwakeError("기존 시스템 잠자기 차단 설정이 남아 있습니다. 해당 설정을 복구한 뒤 다시 시작해 주세요.")
        }
    }

    func stop() {
        if assertion != 0 { IOPMAssertionRelease(assertion); assertion = 0 }
    }
    deinit { stop() }
}
