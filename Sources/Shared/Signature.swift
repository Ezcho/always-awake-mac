import Foundation
import Security

enum Signature {
    // A production identity yields a Team ID requirement. Ad-hoc development builds
    // are pinned to their exact designated requirement; there is no identifier-only bypass.
    static func requirement(for url: URL) throws -> String {
        var code: SecStaticCode?
        try check(SecStaticCodeCreateWithPath(url as CFURL, [], &code))
        guard let code else { throw AwakeError("서명 정보를 읽지 못했습니다.") }
        try check(SecStaticCodeCheckValidity(code, SecCSFlags(rawValue: kSecCSStrictValidate | kSecCSCheckNestedCode), nil))
        var requirement: SecRequirement?
        try check(SecCodeCopyDesignatedRequirement(code, [], &requirement))
        guard let requirement else { throw AwakeError("서명 요구 사항을 읽지 못했습니다.") }
        var text: CFString?
        try check(SecRequirementCopyString(requirement, [], &text))
        guard let text else { throw AwakeError("서명 요구 사항이 비어 있습니다.") }
        return text as String
    }

    private static func check(_ status: OSStatus) throws {
        guard status == errSecSuccess else { throw AwakeError("앱 서명 검증에 실패했습니다 (\(status)). 앱을 다시 설치해 주세요.") }
    }
}
