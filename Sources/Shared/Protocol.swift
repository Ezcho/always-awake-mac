import Foundation

enum AppIdentity {
    static let bundleID = "com.alwaysawake.mac"
    static let helperID = "com.alwaysawake.mac.helper"
    static let serviceName = "com.alwaysawake.mac.helper"
    static let helperPlist = "com.alwaysawake.mac.helper.plist"
    static let version = "1.0.9"
}

// Only fixed power operations cross the privileged boundary. No commands or paths.
@objc protocol AwakeServiceProtocol {
    func beginSession(reply: @escaping (Data) -> Void)
    func endSession(reply: @escaping (Data) -> Void)
    func heartbeat(reply: @escaping (Data) -> Void)
    func status(reply: @escaping (Data) -> Void)
}

struct ServiceReply: Codable {
    var active: Bool
    var message: String?
    var recoveryRequired: Bool
    var ownedByCaller: Bool

    init(active: Bool = false, message: String? = nil, recoveryRequired: Bool = false, ownedByCaller: Bool = false) {
        self.active = active
        self.message = message
        self.recoveryRequired = recoveryRequired
        self.ownedByCaller = ownedByCaller
    }

    var data: Data { (try? JSONEncoder().encode(self)) ?? Data() }
}
