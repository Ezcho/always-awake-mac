import Foundation

/// pmset omits SleepDisabled when the valid system settings dictionary has no
/// override. Apple's PMActivateSystemPowerSettings treats that absence as false.
/// An absent header, malformed value, or duplicate key is still an error.
enum SleepSetting {
    static func disabled(in text: String) throws -> Bool {
        var systemSettings = false
        var value: Bool?
        for line in text.split(separator: "\n") {
            let trimmed = line.trimmingCharacters(in: .whitespaces)
            if trimmed == "System-wide power settings:" { systemSettings = true }
            let fields = line.split(whereSeparator: { $0.isWhitespace })
            guard fields.first == "SleepDisabled" else { continue }
            guard value == nil, fields.count == 2, fields[1] == "0" || fields[1] == "1" else {
                throw AwakeError("잠자기 설정 응답이 올바르지 않습니다.")
            }
            value = fields[1] == "1"
        }
        if let value { return value }
        guard systemSettings else { throw AwakeError("현재 잠자기 설정을 확인할 수 없습니다.") }
        return false
    }
}
