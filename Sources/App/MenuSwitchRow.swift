import AppKit

/// Standard macOS text and switches; no window, animations or rendering timer.
@MainActor
final class MenuSwitchRow: NSView {
    private let label: NSTextField
    let control = NSSwitch()
    var action: (() -> Void)?

    init(title: String) {
        label = NSTextField(labelWithString: title)
        super.init(frame: NSRect(x: 0, y: 0, width: 216, height: 32))
        label.font = .menuFont(ofSize: 13)
        label.frame = NSRect(x: 16, y: 8, width: 125, height: 17)
        control.controlSize = .small
        control.sizeToFit()
        control.frame.origin = NSPoint(x: 216 - 16 - control.frame.width, y: (32 - control.frame.height) / 2)
        control.target = self
        control.action = #selector(toggled)
        control.setAccessibilityLabel(title)
        addSubview(label)
        addSubview(control)
    }

    required init?(coder: NSCoder) { nil }

    func update(on: Bool, enabled: Bool) {
        control.state = on ? .on : .off
        control.isEnabled = enabled
        label.textColor = enabled ? .labelColor : .disabledControlTextColor
        control.setAccessibilityValue(on ? "ON" : "OFF")
    }

    @objc private func toggled() { action?() }
    override func mouseUp(with event: NSEvent) {
        if control.isEnabled { action?() }
    }
}
