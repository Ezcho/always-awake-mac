import Foundation

// Keep command-line repair subject to the same idle-state checks as the UI.
// Only a definite absent app permits proceeding without a status response.
enum ServiceRepairPolicy {
    static func requireLegacyRepair(installedHelperPresent: Bool) throws {
        guard !installedHelperPresent else {
            throw AwakeError("통합 PKG로 설치된 보조 서비스입니다. 기존 서비스 등록 명령 대신 현재 버전의 pika PKG를 다시 설치해 주세요.")
        }
    }

    static func requireIdleApplication(_ reply: [String: Any]) throws {
        if reply["ok"] as? Bool == true {
            guard reply["sessionOn"] as? Bool == false,
                  reply["recoveryRequired"] as? Bool == false,
                  reply["busy"] as? Bool == false else {
                throw AwakeError("먼저 pika의 Session을 OFF로 바꾸고 복구가 끝날 때까지 기다려 주세요.")
            }
            return
        }
        guard reply["code"] as? String == "app_not_running" else {
            throw AwakeError("pika의 실행 상태를 확인하지 못해 보조 서비스를 변경하지 않았습니다. 앱을 확인하고 다시 시도해 주세요.")
        }
    }
}
