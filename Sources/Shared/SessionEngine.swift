import Foundation

protocol SleepDriver: AnyObject {
    func sleepIsDisabled() throws -> Bool
    func setSleepDisabled(_ disabled: Bool) throws
}

protocol RecoveryJournal: AnyObject {
    func hasRecoveryRecord() throws -> Bool
    func saveRecoveryRecord() throws
    func clearRecoveryRecord() throws
}

struct AwakeError: LocalizedError {
    let message: String
    init(_ message: String) { self.message = message }
    var errorDescription: String? { message }
}

// Access only from one serial queue. A persisted intent precedes every power change.
final class SessionEngine {
    private let driver: SleepDriver
    private let journal: RecoveryJournal
    private let now: () -> TimeInterval
    private let leaseDuration: TimeInterval
    private(set) var owner: UUID?
    private var expiresAt: TimeInterval = 0
    private(set) var recoveryRequired = false
    private var ownsRecoveryRecord = false
    private(set) var lastMessage: String?

    init(driver: SleepDriver, journal: RecoveryJournal, leaseDuration: TimeInterval = 35,
         now: @escaping () -> TimeInterval = { ProcessInfo.processInfo.systemUptime }) {
        self.driver = driver
        self.journal = journal
        self.leaseDuration = leaseDuration
        self.now = now
        recover()
    }

    func recover() {
        do {
            if try journal.hasRecoveryRecord() {
                ownsRecoveryRecord = true
                recoveryRequired = true
                try restore()
            }
            lastMessage = nil
        } catch {
            recoveryRequired = true
            lastMessage = "잠자기 설정을 복구하지 못했습니다. \(error.localizedDescription)"
        }
    }

    func begin(owner candidate: UUID, safetyIssue: String?) throws {
        if let safetyIssue { throw AwakeError(safetyIssue) }
        if owner == candidate { try renew(owner: candidate, safetyIssue: safetyIssue); return }
        guard owner == nil else { throw AwakeError("다른 Always Awake 창에서 세션을 사용 중입니다.") }
        if recoveryRequired { recover() }
        guard !recoveryRequired else { throw AwakeError(lastMessage ?? "잠자기 설정 복구가 필요합니다.") }
        guard try !driver.sleepIsDisabled() else {
            throw AwakeError("다른 앱 또는 시스템 설정이 이미 잠자기를 차단하고 있습니다. 해당 기능을 먼저 꺼 주세요.")
        }
        try journal.saveRecoveryRecord()
        ownsRecoveryRecord = true
        recoveryRequired = true
        do {
            try driver.setSleepDisabled(true)
            guard try driver.sleepIsDisabled() else { throw AwakeError("이 Mac에서 덮개 잠자기 방지가 적용되지 않았습니다.") }
            owner = candidate
            expiresAt = now() + leaseDuration
            lastMessage = nil
        } catch {
            let initialError = error
            do { try restore() } catch { lastMessage = "설정 복구가 필요합니다. \(error.localizedDescription)" }
            throw initialError
        }
    }

    func renew(owner candidate: UUID, safetyIssue: String?) throws {
        guard owner == candidate else { throw AwakeError(lastMessage ?? "세션이 종료되었습니다. 다시 켜 주세요.") }
        if let safetyIssue {
            try stop(reason: safetyIssue)
            throw AwakeError(safetyIssue)
        }
        guard now() < expiresAt else {
            try stop(reason: "앱의 응답이 없어 세션을 종료했습니다.")
            throw AwakeError(lastMessage!)
        }
        guard try driver.sleepIsDisabled() else {
            try stop(reason: "시스템 잠자기 설정이 변경되어 세션을 종료했습니다.")
            throw AwakeError(lastMessage!)
        }
        expiresAt = now() + leaseDuration
    }

    func end(owner candidate: UUID) throws {
        guard owner == nil || owner == candidate else { throw AwakeError("다른 세션을 종료할 수 없습니다.") }
        try stop(reason: nil)
    }

    func disconnected(owner candidate: UUID) {
        guard owner == candidate else { return }
        do { try stop(reason: "앱 연결이 종료되어 잠자기 설정을 복구했습니다.") }
        catch { lastMessage = error.localizedDescription }
    }

    func tick(safetyIssue: String?) {
        if owner != nil, let safetyIssue {
            do { try stop(reason: safetyIssue) } catch { lastMessage = error.localizedDescription }
        } else if owner != nil && now() >= expiresAt {
            do { try stop(reason: "앱의 응답이 없어 세션을 종료했습니다.") } catch { lastMessage = error.localizedDescription }
        } else if owner == nil && recoveryRequired {
            // Retry failed restoration without dropping the recovery record.
            if ownsRecoveryRecord {
                do { try restore() } catch { lastMessage = error.localizedDescription }
            } else { recover() }
        }
    }

    func shutdown() throws { try stop(reason: nil) }

    func reply(for candidate: UUID, error: Error? = nil) -> ServiceReply {
        ServiceReply(active: owner != nil, message: error?.localizedDescription ?? lastMessage,
                     recoveryRequired: recoveryRequired && owner == nil, ownedByCaller: owner == candidate)
    }

    private func stop(reason: String?) throws {
        owner = nil
        expiresAt = 0
        lastMessage = reason
        if recoveryRequired { try restore() }
    }

    private func restore() throws {
        guard ownsRecoveryRecord else { throw AwakeError("유효한 복구 기록이 없어 설정을 변경하지 않았습니다.") }
        try driver.setSleepDisabled(false)
        guard try !driver.sleepIsDisabled() else { throw AwakeError("macOS가 잠자기 설정 복구를 거부했습니다.") }
        try journal.clearRecoveryRecord()
        recoveryRequired = false
        ownsRecoveryRecord = false
    }
}
