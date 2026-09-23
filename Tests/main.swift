import Foundation

final class FakeDriver: SleepDriver {
    var disabled = false
    var failEnable = false
    var failRestore = false
    var ignoreEnable = false
    var changes: [Bool] = []
    func sleepIsDisabled() throws -> Bool { disabled }
    func setSleepDisabled(_ value: Bool) throws {
        changes.append(value)
        if value && failEnable || !value && failRestore { throw AwakeError("Simulated power failure") }
        if value && ignoreEnable { return }
        disabled = value
    }
}
final class FakeJournal: RecoveryJournal {
    var stored = false
    var failSave = false
    var failClear = false
    var failRead = false
    func hasRecoveryRecord() throws -> Bool {
        if failRead { throw AwakeError("Invalid recovery record") }
        return stored
    }
    func saveRecoveryRecord() throws {
        if failSave { throw AwakeError("Simulated disk failure") }
        stored = true
    }
    func clearRecoveryRecord() throws {
        if failClear { throw AwakeError("Simulated disk removal failure") }
        stored = false
    }
}

var count = 0
func test(_ name: String, _ run: () throws -> Void) {
    do { try run(); count += 1; print("PASS \(name)") }
    catch { print("FAIL \(name): \(error)"); exit(1) }
}
func expect(_ condition: @autoclosure () -> Bool, _ message: String = "Assertion failed") throws {
    if !condition() { throw AwakeError(message) }
}
func mustFail(_ run: () throws -> Void) throws {
    do { try run() } catch { return }
    throw AwakeError("Expected failure")
}
func fixture() -> (SessionEngine, FakeDriver, FakeJournal) {
    let d = FakeDriver(); let j = FakeJournal()
    return (SessionEngine(driver: d, journal: j), d, j)
}

test("Session ON/OFF restores sleep and clears recovery intent") {
    let (e, d, j) = fixture(); let id = UUID()
    try e.begin(owner: id, safetyIssue: nil)
    try expect(d.disabled && j.stored && e.owner == id)
    try e.end(owner: id)
    try expect(!d.disabled && !j.stored && e.owner == nil && !e.recoveryRequired)
}
test("No mutation when another tool already disabled sleep") {
    let (e, d, j) = fixture(); d.disabled = true
    try mustFail { try e.begin(owner: UUID(), safetyIssue: nil) }
    try expect(d.disabled && !j.stored && d.changes.isEmpty)
}
test("Journal failure prevents all power changes") {
    let (e, d, j) = fixture(); j.failSave = true
    try mustFail { try e.begin(owner: UUID(), safetyIssue: nil) }
    try expect(!d.disabled && d.changes.isEmpty)
}
test("Failed activation rolls back") {
    let (e, d, j) = fixture(); d.failEnable = true
    try mustFail { try e.begin(owner: UUID(), safetyIssue: nil) }
    try expect(!d.disabled && !j.stored && e.owner == nil)
}
test("OS silently ignoring disable is reported as failure") {
    let (e, d, _) = fixture(); d.ignoreEnable = true
    try mustFail { try e.begin(owner: UUID(), safetyIssue: nil) }
    try expect(e.owner == nil)
}
test("Crash disconnect releases power override") {
    let (e, d, _) = fixture(); let id = UUID()
    try e.begin(owner: id, safetyIssue: nil); e.disconnected(owner: id)
    try expect(!d.disabled && e.owner == nil)
}
test("Only the owning connection can stop or renew") {
    let (e, d, _) = fixture(); let id = UUID()
    try e.begin(owner: id, safetyIssue: nil)
    try mustFail { try e.end(owner: UUID()) }
    try mustFail { try e.renew(owner: UUID(), safetyIssue: nil) }
    e.disconnected(owner: UUID())
    try expect(d.disabled && e.owner == id)
}
test("Helper restart recovers persisted override") {
    let d = FakeDriver(); let j = FakeJournal(); d.disabled = true; j.stored = true
    let e = SessionEngine(driver: d, journal: j)
    try expect(!d.disabled && !j.stored && !e.recoveryRequired)
}
test("Recovery failure retains journal and watchdog retries") {
    let (e, d, j) = fixture(); let id = UUID()
    try e.begin(owner: id, safetyIssue: nil); d.failRestore = true
    try mustFail { try e.end(owner: id) }
    try expect(j.stored && e.recoveryRequired && e.owner == nil)
    d.failRestore = false; e.tick(safetyIssue: nil)
    try expect(!j.stored && !d.disabled && !e.recoveryRequired)
}
test("A stalled app loses its lease, even when its process remains alive") {
    let d = FakeDriver(); let j = FakeJournal(); var now: TimeInterval = 100
    let e = SessionEngine(driver: d, journal: j, now: { now }); let id = UUID()
    try e.begin(owner: id, safetyIssue: nil)
    now = 130; try e.renew(owner: id, safetyIssue: nil)
    now = 164; e.tick(safetyIssue: nil); try expect(d.disabled)
    now = 165; e.tick(safetyIssue: nil); try expect(!d.disabled)
}
test("Late heartbeat cannot resurrect expired lease") {
    let d = FakeDriver(); let j = FakeJournal(); var now: TimeInterval = 0
    let e = SessionEngine(driver: d, journal: j, now: { now }); let id = UUID()
    try e.begin(owner: id, safetyIssue: nil); now = 36
    try mustFail { try e.renew(owner: id, safetyIssue: nil) }
    try expect(!d.disabled)
}
test("Safety event ends session without losing recovery intent") {
    let (e, d, _) = fixture(); try e.begin(owner: UUID(), safetyIssue: nil)
    e.tick(safetyIssue: "Battery low")
    try expect(!d.disabled && e.owner == nil && e.lastMessage == "Battery low")
}
test("Unsafe start is rejected") {
    let (e, d, _) = fixture()
    try mustFail { try e.begin(owner: UUID(), safetyIssue: "Too hot") }
    try expect(d.changes.isEmpty)
}
test("External setting change terminates session") {
    let (e, d, _) = fixture(); let id = UUID(); try e.begin(owner: id, safetyIssue: nil)
    d.disabled = false
    try mustFail { try e.renew(owner: id, safetyIssue: nil) }
    try expect(e.owner == nil)
}
test("Closed headless Mac uses 25% / serious threshold") {
    var s = SafetyReading(batteryPercent: 26, onAC: false, lidClosed: true, hasExternalDisplay: false, heat: .normal)
    try expect(s.profile == .closed && s.issue == nil)
    s.batteryPercent = 25; try expect(s.issue != nil)
    s.batteryPercent = 90; s.heat = .serious; try expect(s.issue != nil)
    s.onAC = true; try expect(s.issue != nil)
}
test("Desktop requires BOTH AC and external display; tolerates serious heat") {
    var s = SafetyReading(batteryPercent: 10, onAC: true, lidClosed: true, hasExternalDisplay: true, heat: .serious)
    try expect(s.profile == .desktop && s.issue == nil)
    s.heat = .critical; try expect(s.issue != nil)
    s.onAC = false; try expect(s.profile == .portable && s.issue != nil)
}
test("Unplugging display while closed immediately tightens protection") {
    var s = SafetyReading(batteryPercent: 20, onAC: true, lidClosed: true, hasExternalDisplay: true, heat: .serious)
    try expect(s.issue == nil)
    s.hasExternalDisplay = false; try expect(s.profile == .closed && s.issue != nil)
}
test("Portable battery cutoff is inclusive at 15%") {
    var s = SafetyReading(batteryPercent: 16, onAC: false, lidClosed: false, hasExternalDisplay: false, heat: .serious)
    try expect(s.issue == nil)
    s.batteryPercent = 15; try expect(s.issue != nil)
}
test("Unknown battery blocks unattended headless battery session") {
    let s = SafetyReading(batteryPercent: nil, onAC: false, lidClosed: true, hasExternalDisplay: false, heat: .normal)
    try expect(s.issue != nil)
}
test("Corrupt recovery record cannot overwrite an unrelated power setting") {
    let d = FakeDriver(); let j = FakeJournal(); d.disabled = true; j.failRead = true
    let e = SessionEngine(driver: d, journal: j)
    e.tick(safetyIssue: nil)
    try expect(e.recoveryRequired && d.changes.isEmpty && d.disabled)
}
test("Failed journal removal preserves retry even after sleep was restored") {
    let (e, d, j) = fixture(); let id = UUID()
    try e.begin(owner: id, safetyIssue: nil); j.failClear = true
    try mustFail { try e.end(owner: id) }
    try expect(!d.disabled && j.stored && e.recoveryRequired)
    j.failClear = false; e.tick(safetyIssue: nil)
    try expect(!j.stored && !e.recoveryRequired)
}
print("\(count) tests passed. No system power settings were modified.")
