import Foundation
import Security
import Darwin

// Installer-managed files have a separate service identity from SMAppService.
// Nothing here installs files, elevates privileges, or relaxes signature checks.
enum InstalledHelper {
    static let serviceName = "com.alwaysawake.mac.installed.helper"
    static let executable = URL(fileURLWithPath: "/Library/PrivilegedHelperTools/" + serviceName)
    static let plist = URL(fileURLWithPath: "/Library/LaunchDaemons/" + serviceName + ".plist")
    static let manifest = URL(fileURLWithPath: "/Library/Application Support/pika/installed-client.requirement")

    static var isPresent: Bool {
        [executable, plist, manifest].contains { url in
            var info = stat()
            return lstat(url.path, &info) == 0 || errno != ENOENT
        }
    }

    static func validateProtectedFile(_ url: URL) throws {
        let components = url.pathComponents
        guard components.first == "/", !components.contains(".."), !components.contains(".") else {
            throw AwakeError("설치 경로가 올바르지 않습니다.")
        }
        var path = ""
        for (index, component) in components.enumerated() {
            path = index == 0 ? "/" : (path as NSString).appendingPathComponent(component)
            var info = stat()
            guard lstat(path, &info) == 0,
                  info.st_uid == 0, info.st_mode & 0o022 == 0,
                  info.st_mode & S_IFMT == (index == components.count - 1 ? S_IFREG : S_IFDIR) else {
                throw AwakeError("설치 파일의 소유자·권한·경로 검증에 실패했습니다. pika 설치 패키지로 다시 설치해 주세요.")
            }
        }
    }

    static func clientRequirement() throws -> String {
        try validateProtectedFile(executable)
        try validateProtectedFile(manifest)
        try validateProtectedFile(plist)
        let attributes = try FileManager.default.attributesOfItem(atPath: manifest.path)
        guard let size = attributes[.size] as? NSNumber, size.intValue > 0, size.intValue < 16_384 else {
            throw AwakeError("설치된 앱 서명 정보의 크기가 올바르지 않습니다.")
        }
        let value = try String(contentsOf: manifest, encoding: .utf8).trimmingCharacters(in: .whitespacesAndNewlines)
        _ = try requirement(value)
        let data = try Data(contentsOf: plist)
        guard let info = try PropertyListSerialization.propertyList(from: data, format: nil) as? [String: Any],
              info["Label"] as? String == serviceName,
              info["ProgramArguments"] as? [String] == [executable.path],
              (info["MachServices"] as? [String: Any])?[serviceName] as? Bool == true,
              info["BundleProgram"] == nil else {
            throw AwakeError("설치된 보조 서비스 설정이 올바르지 않습니다.")
        }
        return value
    }

    static func validateForClient(app: URL = Bundle.main.bundleURL) throws {
        let clientPin = try clientRequirement()
        try validateSignature(app, requirement: clientPin)
        let bundled = app.appendingPathComponent("Contents/Library/HelperTools/AlwaysAwakeHelper")
        let helperPin = try Signature.requirement(for: bundled)
        try validateSignature(executable, requirement: helperPin)
    }

    private static func requirement(_ text: String) throws -> SecRequirement {
        var value: SecRequirement?
        guard SecRequirementCreateWithString(text as CFString, [], &value) == errSecSuccess, let value else {
            throw AwakeError("설치된 앱 서명 조건을 읽지 못했습니다.")
        }
        return value
    }

    private static func validateSignature(_ url: URL, requirement text: String) throws {
        var code: SecStaticCode?
        guard SecStaticCodeCreateWithPath(url as CFURL, [], &code) == errSecSuccess, let code,
              SecStaticCodeCheckValidity(code, SecCSFlags(rawValue: kSecCSStrictValidate | kSecCSCheckNestedCode),
                                        try requirement(text)) == errSecSuccess else {
            throw AwakeError("앱과 설치된 보조 서비스의 버전·서명이 일치하지 않습니다. pika 설치 패키지로 함께 업데이트해 주세요.")
        }
    }
}
