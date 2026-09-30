import Foundation
import IOKit.pwr_mgt

final class DisplayController {
    private var assertion: IOPMAssertionID = 0
    private var pendingSleep: DispatchWorkItem?
    private var sleepRequest: UUID?
    private var sessionEnabled = false
    var onError: ((String) -> Void)?

    func arm() {
        release()
        sessionEnabled = true
    }

    func disarm() {
        sessionEnabled = false
        release()
    }

    func apply(keepOn: Bool) throws {
        release()
        // Both conditions are mandatory for every display operation, including
        // callers whose cached lid state has not caught up with a reopened lid.
        guard sessionEnabled, HardwareReading.lidIsClosed() == true else { return }
        if keepOn {
            let result = IOPMAssertionCreateWithName(kIOPMAssertionTypePreventUserIdleDisplaySleep as CFString,
                IOPMAssertionLevel(kIOPMAssertionLevelOn), "pika · Monitor ON" as CFString, &assertion)
            guard result == kIOReturnSuccess else { assertion = 0; throw AwakeError("화면 켜짐 설정을 적용하지 못했습니다 (\(result)).") }
            var activity: IOPMAssertionID = 0
            IOPMAssertionDeclareUserActivity("pika · Wake display" as CFString, kIOPMUserActiveLocal, &activity)
            if activity != 0 { IOPMAssertionRelease(activity) }
        } else {
            let request = UUID()
            sleepRequest = request
            let task = DispatchWorkItem { [weak self] in
                guard let self, self.sessionEnabled, self.sleepRequest == request,
                      HardwareReading.lidIsClosed() == true else { return }
                self.sleepRequest = nil
                let process = Process()
                process.executableURL = URL(fileURLWithPath: "/usr/bin/pmset")
                process.arguments = ["displaysleepnow"]
                process.terminationHandler = { [weak self] result in
                    if result.terminationStatus != 0 {
                        DispatchQueue.main.async { self?.onError?("화면을 끄지 못했습니다. Monitor를 다시 전환해 주세요.") }
                    }
                }
                do { try process.run() } catch { self.onError?("화면 잠자기 요청 실패: \(error.localizedDescription)") }
            }
            pendingSleep = task
            DispatchQueue.main.asyncAfter(deadline: .now() + 3, execute: task)
        }
    }

    func release() {
        sleepRequest = nil
        pendingSleep?.cancel()
        pendingSleep = nil
        if assertion != 0 { IOPMAssertionRelease(assertion); assertion = 0 }
    }
    deinit { release() }
}
