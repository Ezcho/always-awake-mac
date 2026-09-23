import Foundation

enum HeatLevel: Int, Codable, Comparable {
    case normal, fair, serious, critical
    static func < (lhs: HeatLevel, rhs: HeatLevel) -> Bool { lhs.rawValue < rhs.rawValue }
    var label: String {
        switch self { case .normal: return "정상"; case .fair: return "주의"; case .serious: return "높음"; case .critical: return "위험" }
    }
}

enum SafetyProfile: String, Codable {
    case closed, portable, desktop
    var title: String {
        switch self { case .closed: return "덮개 닫힘 · 엄격 보호"; case .portable: return "일반 보호"; case .desktop: return "Desktop 보호" }
    }
    var batteryFloor: Int { self == .closed ? 25 : 15 }
    var heatCeiling: HeatLevel { self == .closed ? .serious : .critical }
    var detail: String {
        switch self {
        case .closed: return "배터리 25% 이하 또는 열 상태 높음부터 잠자기"
        case .portable: return "배터리 15% 이하 또는 열 상태 위험 시 잠자기"
        case .desktop: return "전원 + 외장 화면 연결 · 열 상태 위험 시 잠자기"
        }
    }
}

struct SafetyReading: Codable {
    var batteryPercent: Int?
    var onAC: Bool
    var lidClosed: Bool
    var hasExternalDisplay: Bool
    var heat: HeatLevel

    var profile: SafetyProfile {
        if lidClosed && !hasExternalDisplay { return .closed }
        if onAC && hasExternalDisplay { return .desktop }
        return .portable
    }
    var issue: String? {
        if heat >= profile.heatCeiling { return "\(profile.title): 열 상태가 ‘\(heat.label)’이라 Mac을 잠자기로 전환합니다." }
        if !onAC, let batteryPercent, batteryPercent <= profile.batteryFloor {
            return "\(profile.title): 배터리가 \(batteryPercent)%라 Mac을 잠자기로 전환합니다. 전원을 연결해 주세요."
        }
        // Unknown battery readings on a laptop must not permit an unattended headless session.
        if lidClosed && !hasExternalDisplay && !onAC && batteryPercent == nil {
            return "배터리 상태를 확인할 수 없어 Mac을 잠자기로 전환합니다."
        }
        return nil
    }
}
