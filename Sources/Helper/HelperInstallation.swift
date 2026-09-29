import Foundation
import MachO

enum HelperInstallation {
    static func appURL() throws -> URL {
        // launchd may supply the relative BundleProgram as argv[0]. dyld knows
        // the executable that was actually loaded, independent of argv or cwd.
        var size: UInt32 = 0
        _ = _NSGetExecutablePath(nil, &size)
        guard size > 0 else { throw AwakeError("보조 서비스 실행 경로를 찾지 못했습니다.") }
        var buffer = [CChar](repeating: 0, count: Int(size))
        guard _NSGetExecutablePath(&buffer, &size) == 0 else {
            throw AwakeError("보조 서비스 실행 경로를 읽지 못했습니다.")
        }
        let executable = URL(fileURLWithPath: String(cString: buffer)).resolvingSymlinksInPath()
        let app = executable.deletingLastPathComponent().deletingLastPathComponent()
            .deletingLastPathComponent().deletingLastPathComponent()
        guard app.pathExtension == "app",
              executable == app.appendingPathComponent("Contents/Library/HelperTools/AlwaysAwakeHelper") else {
            throw AwakeError("보조 서비스가 앱 내부의 올바른 위치에 설치되지 않았습니다.")
        }
        return app
    }
}
