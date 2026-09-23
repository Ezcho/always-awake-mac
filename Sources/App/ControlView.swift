import SwiftUI

private let accent = Color(red: 0.65, green: 0.96, blue: 0.76)
private let ink = Color(red: 0.055, green: 0.075, blue: 0.071)

struct ControlView: View {
    @ObservedObject var model: AppModel
    var snapshot = false

    var body: some View {
        Group {
            if snapshot {
                content
            } else {
                ScrollView(.vertical) { content }
                    .frame(width: 400, height: min(690, (NSScreen.main?.visibleFrame.height ?? 790) - 100))
            }
        }
        .background(LinearGradient(colors: [Color(red: 0.08, green: 0.115, blue: 0.105), ink], startPoint: .topLeading, endPoint: .bottomTrailing))
        .foregroundStyle(.white).preferredColorScheme(.dark)
    }

    private var content: some View {
        VStack(spacing: 0) {
            HStack(spacing: 9) {
                Image(systemName: "power").font(.system(size: 17, weight: .bold)).foregroundStyle(accent)
                Text("Always Awake").font(.system(size: 16, weight: .semibold))
                Spacer()
                Text("FOR MAC").font(.system(size: 9, weight: .bold, design: .monospaced)).tracking(1.4).foregroundStyle(.white.opacity(0.35))
            }
            .padding(.top, 28).padding(.bottom, 20)

            HStack(spacing: 6) {
                Circle().fill(model.active ? accent : .white.opacity(0.3)).frame(width: 5, height: 5)
                Text(model.recoveryRequired ? "RECOVERY" : model.active ? "SESSION RUNNING" : "READY WHEN YOU ARE")
                    .font(.system(size: 10, weight: .medium, design: .monospaced)).tracking(1.6)
                    .foregroundStyle(model.active ? accent : .white.opacity(0.45))
            }
            .padding(.bottom, 17)

            Button { model.toggleSession() } label: {
                ZStack {
                    Circle().stroke(accent.opacity(model.active ? 0.13 : 0.04), lineWidth: 1).frame(width: 144, height: 144)
                    Circle().fill(model.active ? accent.opacity(0.10) : .white.opacity(0.025)).frame(width: 132, height: 132)
                    Circle().stroke(model.active ? accent.opacity(0.75) : .white.opacity(0.14), lineWidth: 1.5).frame(width: 132, height: 132)
                    Image(systemName: "power").font(.system(size: 46, weight: .light)).foregroundStyle(model.active ? accent : .white.opacity(0.5))
                    if model.busy { ProgressView().scaleEffect(0.7).offset(y: 47) }
                }
                .contentShape(Circle())
            }
            .buttonStyle(.plain).disabled(model.busy)
            .accessibilityLabel(model.active ? "Session 끄기" : "Session 켜기")
            .help("세션을 켜거나 끕니다")
            .padding(.bottom, 18)

            Text(model.recoveryRequired ? "설정을 복구하고 있어요" : model.active ? "작업은 계속됩니다." : "쉬지 않는 Mac, 한 번의 클릭.")
                .font(.system(size: 23, weight: .semibold)).tracking(-0.6)
            Text(model.active ? "덮개를 닫아도, 화면을 꺼도." : "준비가 되면 세션을 켜세요.")
                .font(.system(size: 12)).foregroundStyle(.white.opacity(0.45)).padding(.top, 7)

            VStack(spacing: 0) {
                HStack(spacing: 12) {
                    Image(systemName: "bolt.fill").foregroundStyle(model.active ? accent : .white.opacity(0.55)).frame(width: 19)
                    VStack(alignment: .leading, spacing: 4) {
                        Text("Session").font(.system(size: 14, weight: .medium))
                        Text(model.active ? model.elapsed : "Mac을 깨어 있게 유지")
                            .font(.system(size: 11, design: model.active ? .monospaced : .default)).foregroundStyle(.white.opacity(0.42))
                    }
                    Spacer()
                    switchControl(on: model.active, label: "Session") { model.toggleSession() }
                }.padding(17)
                Rectangle().fill(.white.opacity(0.065)).frame(height: 1).padding(.horizontal, 17)
                HStack(spacing: 12) {
                    Image(systemName: model.monitorOn ? "display" : "moon.zzz").foregroundStyle(.white.opacity(0.55)).frame(width: 19)
                    VStack(alignment: .leading, spacing: 4) {
                        Text("Monitor").font(.system(size: 14, weight: .medium))
                        Text(model.monitorOn ? "세션 중 화면 켜짐 유지" : "세션 중 3초 뒤 화면만 끄기")
                            .font(.system(size: 11)).foregroundStyle(.white.opacity(0.42))
                    }
                    Spacer()
                    switchControl(on: model.monitorOn, label: "Monitor") { model.setMonitor(!model.monitorOn) }
                }.padding(17)
            }
            .background(.white.opacity(0.035), in: RoundedRectangle(cornerRadius: 16))
            .overlay(RoundedRectangle(cornerRadius: 16).strokeBorder(.white.opacity(0.065)))
            .padding(.top, 26)

            if !model.serviceReady {
                Button { model.prepareService() } label: {
                    HStack(spacing: 9) {
                        Image(systemName: "lock.shield")
                        VStack(alignment: .leading, spacing: 3) {
                            Text(model.needsApproval ? "macOS에서 허용하기" : "처음 한 번, 덮개 모드 준비")
                                .font(.system(size: 12, weight: .semibold))
                            Text("보조 서비스 승인 후 한 번의 클릭으로 ON/OFF")
                                .font(.system(size: 10)).foregroundStyle(.white.opacity(0.45))
                        }
                        Spacer()
                        Image(systemName: "arrow.up.right").font(.system(size: 10))
                    }
                    .padding(13).foregroundStyle(accent)
                    .background(accent.opacity(0.055), in: RoundedRectangle(cornerRadius: 11))
                }.buttonStyle(.plain).padding(.top, 12)
            }

            if let error = model.error {
                Text(error).font(.system(size: 11)).foregroundStyle(Color(red: 1, green: 0.77, blue: 0.50))
                    .fixedSize(horizontal: false, vertical: true).frame(maxWidth: .infinity, alignment: .leading).padding(.top, 12)
            }

            VStack(alignment: .leading, spacing: 8) {
                HStack(spacing: 6) {
                    Image(systemName: "shield.lefthalf.filled").foregroundStyle(accent.opacity(0.7))
                    Text(model.hardware.profile.title).foregroundStyle(.white.opacity(0.65))
                    Spacer()
                    Text(model.hardware.onAC ? "전원 연결" : model.hardware.batteryPercent.map { "\($0)%" } ?? "배터리 확인 중")
                        .foregroundStyle(.white.opacity(0.4))
                }.font(.system(size: 10, weight: .medium))
                Text(model.hardware.profile.detail).font(.system(size: 10)).foregroundStyle(.white.opacity(0.35))
                HStack {
                    Text("열 상태: \(model.hardware.heat.label)")
                    Spacer()
                    Text("통풍이 되는 곳에서 사용하세요")
                }.font(.system(size: 10)).foregroundStyle(.white.opacity(0.35))
            }.padding(.top, 20)

            HStack {
                Text("메뉴 막대 클릭: ON/OFF · 우클릭: 이 창")
                    .font(.system(size: 9)).foregroundStyle(.white.opacity(0.3))
                Spacer()
                if snapshot {
                    Image(systemName: "ellipsis").foregroundStyle(.white.opacity(0.5)).frame(width: 20)
                } else { Menu {
                    Button("사용 안내") { openGuide() }
                    if model.serviceReady || model.needsApproval {
                        Button("보조 서비스 제거") { model.removeService() }
                    }
                    Divider()
                    Button("Always Awake 종료") { NSApp.terminate(nil) }.keyboardShortcut("q")
                } label: { Image(systemName: "ellipsis").foregroundStyle(.white.opacity(0.5)) }
                    .menuStyle(.borderlessButton).menuIndicator(.hidden).frame(width: 20)
                }
            }.padding(.top, 18).padding(.bottom, 22)
        }
        .padding(.horizontal, 28).frame(width: 400)
    }

    private func switchControl(on: Bool, label: String, action: @escaping () -> Void) -> some View {
        Button(action: action) {
            HStack(spacing: 6) {
                Text(on ? "ON" : "OFF").font(.system(size: 9, weight: .bold, design: .monospaced))
                    .foregroundStyle(on ? accent : .white.opacity(0.35))
                ZStack(alignment: on ? .trailing : .leading) {
                    Capsule().fill(on ? accent : .white.opacity(0.16)).frame(width: 35, height: 21)
                    Circle().fill(on ? ink : .white.opacity(0.65)).frame(width: 15, height: 15).padding(3)
                }
            }.contentShape(Rectangle())
        }.buttonStyle(.plain).disabled(model.busy).accessibilityLabel("\(label) \(on ? "ON" : "OFF")")
            .accessibilityAddTraits(on ? [.isSelected] : [])
    }

    private func openGuide() {
        if let url = Bundle.main.url(forResource: "Guide", withExtension: "html") { NSWorkspace.shared.open(url) }
    }
}
