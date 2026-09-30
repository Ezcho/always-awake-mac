import Foundation
import IOKit
import IOKit.ps
import CoreGraphics

enum HardwareReading {
    static func lidIsClosed() -> Bool? {
        let root = IOServiceGetMatchingService(kIOMainPortDefault, IOServiceMatching("IOPMrootDomain"))
        guard root != 0 else { return nil }
        defer { IOObjectRelease(root) }
        return IORegistryEntryCreateCFProperty(root, "AppleClamshellState" as CFString, kCFAllocatorDefault, 0)?.takeRetainedValue() as? Bool
    }

    static func current() -> SafetyReading {
        var battery: Int?
        var ac = false
        if let info = IOPSCopyPowerSourcesInfo()?.takeRetainedValue() {
            if let sourceType = IOPSGetProvidingPowerSourceType(info)?.takeUnretainedValue() {
                ac = (sourceType as String) == kIOPSACPowerValue
            }
            if let list = IOPSCopyPowerSourcesList(info)?.takeRetainedValue() as? [CFTypeRef] {
                for item in list {
                    guard let source = IOPSGetPowerSourceDescription(info, item)?.takeUnretainedValue() as? [String: Any],
                          source[kIOPSTypeKey] as? String == kIOPSInternalBatteryType else { continue }
                    ac = source[kIOPSPowerSourceStateKey] as? String == kIOPSACPowerValue
                    if let value = source[kIOPSCurrentCapacityKey] as? Int,
                       let maximum = source[kIOPSMaxCapacityKey] as? Int, maximum > 0 {
                        battery = min(100, max(0, value * 100 / maximum))
                    }
                }
            }
        }
        let closed = lidIsClosed() ?? true
        var displays = [CGDirectDisplayID](repeating: 0, count: 32)
        var count: UInt32 = 0
        // Online displays include sleeping screens; an OFF monitor still counts as connected.
        let result = CGGetOnlineDisplayList(UInt32(displays.count), &displays, &count)
        let external = result == .success && displays.prefix(Int(count)).contains { CGDisplayIsBuiltin($0) == 0 }
        let heat: HeatLevel
        switch ProcessInfo.processInfo.thermalState {
        case .nominal: heat = .normal
        case .fair: heat = .fair
        case .serious: heat = .serious
        case .critical: heat = .critical
        @unknown default: heat = .critical
        }
        return SafetyReading(batteryPercent: battery, onAC: ac, lidClosed: closed, hasExternalDisplay: external, heat: heat)
    }
}
