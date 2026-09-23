import Foundation
import IOKit
import IOKit.ps
import SystemConfiguration
import Darwin

final class SystemSleepDriver: SleepDriver {
    func sleepIsDisabled() throws -> Bool {
        let text = try runPMSet(["-g"])
        for line in text.split(separator: "\n") {
            let fields = line.split(whereSeparator: { $0.isWhitespace })
            if fields.first == "SleepDisabled", fields.count == 2, let value = Int(fields[1]), [0, 1].contains(value) {
                return value == 1
            }
        }
        throw AwakeError("이 macOS에서 잠자기 상태를 확인할 수 없습니다.")
    }

    func setSleepDisabled(_ disabled: Bool) throws {
        _ = try runPMSet(["-a", "disablesleep", disabled ? "1" : "0"])
    }

    private func runPMSet(_ args: [String]) throws -> String {
        let process = Process()
        process.executableURL = URL(fileURLWithPath: "/usr/bin/pmset")
        process.arguments = args
        process.environment = ["PATH": "/usr/bin:/bin:/usr/sbin:/sbin", "LANG": "C"]
        let output = Pipe()
        process.standardOutput = output
        process.standardError = output
        let done = DispatchSemaphore(value: 0)
        process.terminationHandler = { _ in done.signal() }
        try process.run()
        if done.wait(timeout: .now() + 5) == .timedOut {
            process.terminate()
            if done.wait(timeout: .now() + 1) == .timedOut { kill(process.processIdentifier, SIGKILL) }
            throw AwakeError("macOS 전원 설정의 응답 시간이 초과되었습니다.")
        }
        let data = output.fileHandleForReading.readDataToEndOfFile()
        guard process.terminationStatus == 0 else { throw AwakeError("macOS 전원 설정을 변경하지 못했습니다 (\(process.terminationStatus)).") }
        return String(decoding: data, as: UTF8.self)
    }
}

final class DiskRecoveryJournal: RecoveryJournal {
    private let directory = URL(fileURLWithPath: "/Library/Application Support/Always Awake", isDirectory: true)
    private var record: URL { directory.appendingPathComponent("recovery.json") }
    private struct Record: Codable { let version: Int; let originalSleepDisabled: Bool }

    init() throws {
        let fm = FileManager.default
        if !fm.fileExists(atPath: directory.path) {
            try fm.createDirectory(at: directory, withIntermediateDirectories: false, attributes: [.posixPermissions: 0o700, .ownerAccountID: 0])
        }
        let attrs = try fm.attributesOfItem(atPath: directory.path)
        guard attrs[.type] as? FileAttributeType == .typeDirectory,
              attrs[.ownerAccountID] as? Int == 0,
              (attrs[.posixPermissions] as? Int ?? 0) & 0o022 == 0 else {
            throw AwakeError("복구 폴더의 소유자 또는 접근 권한이 올바르지 않습니다.")
        }
    }

    func hasRecoveryRecord() throws -> Bool {
        guard FileManager.default.fileExists(atPath: record.path) else { return false }
        let attrs = try FileManager.default.attributesOfItem(atPath: record.path)
        guard attrs[.type] as? FileAttributeType == .typeRegular,
              attrs[.ownerAccountID] as? Int == 0 else { throw AwakeError("복구 기록이 올바르지 않습니다.") }
        let value = try JSONDecoder().decode(Record.self, from: Data(contentsOf: record))
        guard value.version == 1, !value.originalSleepDisabled else { throw AwakeError("복구 기록의 버전이 올바르지 않습니다.") }
        return true
    }

    func saveRecoveryRecord() throws {
        let data = try JSONEncoder().encode(Record(version: 1, originalSleepDisabled: false))
        try data.write(to: record, options: .atomic)
        try FileManager.default.setAttributes([.posixPermissions: 0o600], ofItemAtPath: record.path)
        // Ensure restoration intent reaches disk before changing a persistent OS setting.
        let fd = open(record.path, O_RDONLY | O_NOFOLLOW)
        guard fd >= 0 else { throw AwakeError("복구 기록을 저장하지 못했습니다.") }
        defer { close(fd) }
        guard fsync(fd) == 0 else { throw AwakeError("복구 기록을 디스크에 기록하지 못했습니다.") }
    }

    func clearRecoveryRecord() throws {
        if FileManager.default.fileExists(atPath: record.path) { try FileManager.default.removeItem(at: record) }
    }
}

enum PowerSafety {
    static func consoleUser() -> uid_t? {
        var uid: uid_t = 0
        guard let name = SCDynamicStoreCopyConsoleUser(nil, &uid, nil) as String?, name != "loginwindow", uid >= 500 else { return nil }
        return uid
    }

    static func issue(ownerUID: uid_t?) -> String? {
        if let ownerUID, consoleUser() != ownerUID { return "사용자가 전환되어 세션을 종료했습니다." }
        return HardwareReading.current().issue
    }

    static func sleepNow() {
        let process = Process()
        process.executableURL = URL(fileURLWithPath: "/usr/bin/pmset")
        process.arguments = ["sleepnow"]
        process.environment = ["PATH": "/usr/bin:/bin:/usr/sbin:/sbin"]
        do { try process.run() } catch { NSLog("Safety sleep failed: %@", error.localizedDescription) }
    }
}
