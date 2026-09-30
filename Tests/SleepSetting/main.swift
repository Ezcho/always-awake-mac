import Foundation
let cases: [(String, Bool?)] = [
    ("System-wide power settings:\n SleepDisabled 0\n", false),
    ("System-wide power settings:\n SleepDisabled 1\n", true),
    ("System-wide power settings:\nCurrently in use:\n sleep 1\n", false),
    ("System-wide power settings:\n DestroyFVKeyOnStandby 1\n", false),
    ("", nil), ("permission denied", nil),
    ("Currently in use:\n sleep 1\n", nil),
    ("System-wide power settings:\n SleepDisabled unknown\n", nil),
    ("System-wide power settings:\n SleepDisabled\n", nil),
    ("System-wide power settings:\n SleepDisabled 0\n SleepDisabled 1\n", nil)
]
for (input, expected) in cases {
    let actual = try? SleepSetting.disabled(in: input)
    precondition(actual == expected, "Unexpected parsing: \(input)")
}
print("PASS \(cases.count) sleep-setting cases, including an unset fresh-install override")
