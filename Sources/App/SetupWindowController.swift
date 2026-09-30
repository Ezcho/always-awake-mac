import AppKit

/// App approval and privileged-helper installation are separate steps. This window
/// can only appear after macOS has already allowed the application to launch.
@MainActor
final class SetupWindowController: NSWindowController {
    private let onInstallHelper: () -> Void
    private let onOpenPrivacySettings: () -> Void
    private let onContinue: () -> Void
    private let helperButton = NSButton(title: "보조 서비스 설치 / 연결", target: nil, action: nil)
    private let continueButton = NSButton(title: "제어창으로", target: nil, action: nil)
    private let helperStatus = NSTextField(wrappingLabelWithString: "")
    private let helperBadge = NSTextField(labelWithString: "2")
    private let ink = NSColor(calibratedRed: 0.16, green: 0.22, blue: 0.18, alpha: 1)
    private let green = NSColor(calibratedRed: 0.19, green: 0.39, blue: 0.27, alpha: 1)

    init(onInstallHelper: @escaping () -> Void,
         onOpenPrivacySettings: @escaping () -> Void,
         onContinue: @escaping () -> Void) {
        self.onInstallHelper = onInstallHelper
        self.onOpenPrivacySettings = onOpenPrivacySettings
        self.onContinue = onContinue
        let window = NSWindow(contentRect: NSRect(x: 0, y: 0, width: 500, height: 548),
                              styleMask: [.titled, .closable, .miniaturizable],
                              backing: .buffered, defer: false)
        window.title = "pika · 시작하기"
        window.isReleasedWhenClosed = false
        window.collectionBehavior = [.moveToActiveSpace]
        window.backgroundColor = NSColor(calibratedRed: 0.98, green: 0.97, blue: 0.93, alpha: 1)
        window.appearance = NSAppearance(named: .aqua)
        super.init(window: window)
        buildContent()
        window.center()
        update(helperReady: false, busy: false, status: nil)
    }

    required init?(coder: NSCoder) { nil }

    func present(helperReady: Bool, busy: Bool, status: String?) {
        update(helperReady: helperReady, busy: busy, status: status)
        NSApp.activate(ignoringOtherApps: true)
        showWindow(nil)
        window?.makeKeyAndOrderFront(nil)
    }

    func update(helperReady: Bool, busy: Bool, status: String?) {
        helperBadge.stringValue = helperReady ? "✓" : "2"
        helperButton.title = busy ? "연결 중…" : helperReady ? "보조 서비스 연결 완료" : "보조 서비스 설치 / 연결"
        helperButton.isEnabled = !helperReady && !busy
        continueButton.isEnabled = !busy
        let message = status?.trimmingCharacters(in: .whitespacesAndNewlines)
        helperStatus.stringValue = (message?.isEmpty == false ? message : nil)
            ?? (helperReady ? "준비됐어요. Session을 켜고 덮개를 닫으세요."
                : "덮개 기능에 필요해요. 설치할 때 관리자 승인을 요청합니다.")
        // Keep the full diagnostic available even if a long system error is truncated.
        helperStatus.toolTip = helperStatus.stringValue
        helperStatus.setAccessibilityValue(helperStatus.stringValue)
    }

    private func buildContent() {
        guard let content = window?.contentView else { return }
        let stack = NSStackView()
        stack.orientation = .vertical
        stack.alignment = .leading
        stack.spacing = 10
        stack.translatesAutoresizingMaskIntoConstraints = false
        content.addSubview(stack)
        NSLayoutConstraint.activate([
            stack.leadingAnchor.constraint(equalTo: content.leadingAnchor, constant: 22),
            stack.trailingAnchor.constraint(equalTo: content.trailingAnchor, constant: -22),
            stack.topAnchor.constraint(equalTo: content.topAnchor, constant: 18),
            stack.bottomAnchor.constraint(lessThanOrEqualTo: content.bottomAnchor, constant: -18)
        ])

        let heading = label("pika, 시작할 준비", size: 23, weight: .bold)
        stack.addArrangedSubview(heading)

        let first = card(badge: NSTextField(labelWithString: "✓"),
                         title: "Applications에 넣고 pika 열기",
                         detail: label("이 창이 보이면 앱 실행 허용은 완료됐어요.", size: 12))
        addFullWidth(first, to: stack)

        helperStatus.font = .systemFont(ofSize: 12)
        helperStatus.textColor = ink
        helperStatus.maximumNumberOfLines = 2
        helperStatus.lineBreakMode = .byTruncatingTail
        helperStatus.heightAnchor.constraint(equalToConstant: 32).isActive = true
        helperButton.bezelStyle = .rounded
        helperButton.target = self
        helperButton.action = #selector(installHelper)
        helperButton.contentTintColor = green
        let second = card(badge: helperBadge, title: "덮개 기능 보조 서비스",
                          detail: helperStatus, button: helperButton)
        addFullWidth(second, to: stack)

        let third = card(badge: NSTextField(labelWithString: "3"),
                         title: "Session ON  →  덮개 닫기",
                         detail: label("덮개가 열려 있을 때는 대기합니다.", size: 12))
        addFullWidth(third, to: stack)

        let security = NSStackView()
        security.orientation = .vertical
        security.alignment = .leading
        security.spacing = 5
        security.addArrangedSubview(label("앱이 열리지 않을 때만", size: 12, weight: .semibold))
        let securityText = label("시스템 설정 → 개인정보 보호 및 보안 → ‘그래도 열기’\n표시된 앱이 pika인지 확인한 뒤 직접 승인해 주세요.", size: 11)
        addFullWidth(securityText, to: security)
        let privacy = NSButton(title: "개인정보 보호 및 보안 열기", target: self, action: #selector(openPrivacySettings))
        let apple = NSButton(title: "Apple 안내 ↗", target: self, action: #selector(openAppleGuide))
        for button in [privacy, apple] {
            button.bezelStyle = .rounded
            button.controlSize = .small
        }
        let links = NSStackView(views: [privacy, apple])
        links.spacing = 8
        security.addArrangedSubview(links)
        addFullWidth(security, to: stack)

        continueButton.bezelStyle = .rounded
        continueButton.target = self
        continueButton.action = #selector(continueToControls)
        continueButton.keyEquivalent = "\r"
        let footer = NSStackView(views: [NSView(), continueButton])
        footer.orientation = .horizontal
        addFullWidth(footer, to: stack)
    }

    private func card(badge: NSTextField, title: String, detail: NSTextField, button: NSButton? = nil) -> NSView {
        let card = NSView()
        card.wantsLayer = true
        card.layer?.backgroundColor = NSColor.white.withAlphaComponent(0.78).cgColor
        card.layer?.cornerRadius = 12
        badge.font = .systemFont(ofSize: 18, weight: .bold)
        badge.textColor = green
        badge.alignment = .center
        badge.translatesAutoresizingMaskIntoConstraints = false
        card.addSubview(badge)
        let body = NSStackView()
        body.orientation = .vertical
        body.alignment = .leading
        body.spacing = 4
        body.translatesAutoresizingMaskIntoConstraints = false
        card.addSubview(body)
        body.addArrangedSubview(label(title, size: 14, weight: .semibold))
        addFullWidth(detail, to: body)
        if let button { body.addArrangedSubview(button) }
        NSLayoutConstraint.activate([
            badge.leadingAnchor.constraint(equalTo: card.leadingAnchor, constant: 10),
            badge.topAnchor.constraint(equalTo: card.topAnchor, constant: 11),
            badge.widthAnchor.constraint(equalToConstant: 26),
            body.leadingAnchor.constraint(equalTo: badge.trailingAnchor, constant: 8),
            body.trailingAnchor.constraint(equalTo: card.trailingAnchor, constant: -12),
            body.topAnchor.constraint(equalTo: card.topAnchor, constant: 10),
            body.bottomAnchor.constraint(equalTo: card.bottomAnchor, constant: -10)
        ])
        return card
    }

    private func label(_ text: String, size: CGFloat, weight: NSFont.Weight = .regular) -> NSTextField {
        let field = NSTextField(wrappingLabelWithString: text)
        field.font = .systemFont(ofSize: size, weight: weight)
        field.textColor = ink
        field.setContentCompressionResistancePriority(.required, for: .vertical)
        return field
    }

    private func addFullWidth(_ view: NSView, to stack: NSStackView) {
        stack.addArrangedSubview(view)
        view.translatesAutoresizingMaskIntoConstraints = false
        view.widthAnchor.constraint(equalTo: stack.widthAnchor).isActive = true
    }

    @objc private func installHelper() { onInstallHelper() }
    @objc private func openPrivacySettings() { onOpenPrivacySettings() }
    @objc private func continueToControls() { close(); onContinue() }
    @objc private func openAppleGuide() {
        if let url = URL(string: "https://support.apple.com/ko-kr/102445") {
            NSWorkspace.shared.open(url)
        }
    }
}
