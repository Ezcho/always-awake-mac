# pika

**Keep your Mac awake from the menu bar.** Session and display controls, battery and thermal monitoring, with a native MCP interface in the development source. macOS 13+, Apple Silicon and Intel.

macOS 메뉴 막대에서 Session과 Monitor를 제어하는 네이티브 앱입니다. Swift / AppKit으로 만들었으며 외부 패키지나 서버 없이 실행됩니다.

[다운로드 페이지](https://no-sleep-pika.online/) · [공개 릴리스](https://github.com/Ezcho/always-awake-mac/releases/tag/v1.0.3-mvp)

웹페이지의 다운로드 수는 공개 GitHub Release의 DMG·ZIP·설치 PKG 다운로드 합계입니다. 제거 패키지와 체크섬 파일은 제외합니다. 고유 사용자 수나 설치 성공 횟수는 아닙니다. 브라우저는 공개 API에서 갱신하고 1시간 캐시합니다. API 연결 실패 시 마지막 집계값을 유지하며, 표시값에 마우스를 올리면 집계 시각을 볼 수 있습니다. 배포용 기본 집계는 `python3 Scripts/update-downloads.py` 후 `python3 Scripts/build-site.py`로 갱신합니다.

> **이 문서는 개발 중인 1.0.4 소스를 설명합니다.** 현재 공개 다운로드는 1.0.3이며 MCP·덮개 대기 동작·새 PKG 설치 경로는 아직 포함되지 않았습니다. 1.0.4는 덮개 닫힘 동작을 위해 관리자 보조 서비스를 사용합니다. 보조 서비스가 없으면 설치를 안내하며 Session을 시작하지 않습니다. 새 `.pkg`의 설치 및 실기 검증은 진행 중입니다. 현재 빌드는 Developer ID 서명·Apple 공증 전입니다.

## 사용

1. DMG를 열고 **pika.app**을 **Applications**로 드래그합니다.
2. 앱과 보조 서비스를 `.pkg`로 설치하고 실행한 뒤, 덮개를 열어 둔 채 **Session ON**을 누릅니다.
3. 덮개 모드에서는 **Session ON → 대기 → 덮개 닫기** 순서로 동작합니다. ON을 누르거나 대기 중 Monitor를 바꿔도 현재 화면을 끄거나 깨우지 않습니다.

메뉴 막대 아이콘 **클릭**으로 Session·Monitor 스위치를 엽니다. **Option+클릭**은 Session을 바로 전환합니다. 실행하면 작은 제어창이 표시됩니다. 창의 X를 눌러 닫아도 Session과 메뉴 막대는 유지됩니다. 앱을 다시 실행하거나 메뉴의 **제어창 열기**로 창을 다시 엽니다. Dock 아이콘은 없습니다. 종료는 메뉴의 **종료**를 사용합니다.

- Session OFF: Monitor 스위치는 OFF로 표시되고 비활성화됩니다. 화면을 즉시 끄지 않으며, 다음 Session에서는 마지막 Monitor 선택을 복원합니다.
- 덮개 모드: 덮개를 닫으면 Monitor 선택을 적용하고, 다시 열면 화면 제어를 해제하고 대기로 돌아갑니다. 닫힘 감지는 약 1초 간격입니다. 덮개 닫힘과 동시에 Mac이 잠들지 않도록 시스템 잠자기 방지는 ON 시 미리 준비합니다.
- Monitor ON은 화면 자동 잠자기를 방지하고, OFF는 적용 시점부터 3초 뒤 화면 잠자기를 요청합니다. 덮개 모드의 대기 중에는 선택만 저장합니다. 화면 잠금은 macOS 설정에 따릅니다.
- Session OFF / 정상 종료: 이 앱이 변경한 시스템 잠자기 설정과 화면 assertion을 해제합니다.
- 다른 앱이 이미 `SleepDisabled=1`을 설정했다면 시작을 거절하여 기존 소유권을 보존합니다.
- 네트워크, AI 서비스 제한, 브라우저 백그라운드 정책, 에이전트 자체 오류·종료는 관리하지 않습니다.

## 과열·방전 보호

보조 서비스는 5초마다 실제 전원·배터리·덮개·외장 화면·macOS 열 상태를 확인합니다. 별도의 복잡한 설정 없이 아래 기준으로 자동 전환합니다. 배터리 기준은 외부 전원 없이 사용할 때 적용합니다.

| 사용 상태 | 배터리 기준 | macOS 열 상태 기준 |
| --- | --- | --- |
| 덮개 닫힘 + 외장 화면 없음 | 25% 이하 | serious(높음) 이상 |
| 일반 사용 / 배터리로 외장 화면 사용 | 15% 이하 | critical(위험) |
| Desktop: 외부 전원 + 외장 화면 | 해당 없음 | critical(위험) |

보조 서비스는 안전 기준에 도달하면 원래 설정을 복구하고 Mac 잠자기를 요청합니다. 작업 프로세스를 강제로 종료하지 않지만 작업을 자동 저장하는 기능은 아닙니다. 안전 중단 후 세션을 자동 재개하지 않습니다. 열 상태는 섭씨 센서값이 아닌 macOS의 thermal pressure입니다. 가방 안 사용의 안전을 보장하지 않으며, 통풍이 되는 곳에서 사용해야 합니다.

이전 Always Awake에서 이름이 pika로 바뀌었습니다. 기존 GitHub 주소와 내부 서비스 식별자는 업데이트 호환성을 위해 유지합니다. 기존 앱은 세션과 보조 서비스를 해제한 뒤 종료하고 pika로 교체하세요.

## 구조와 복구

Session ON은 덮개를 닫기 위한 준비 상태입니다. 이때 보조 서비스가 잠자기 방지와 복구 감시를 미리 준비하며 화면 제어는 하지 않습니다. 덮개가 닫히면 Monitor 선택을 적용하고, 다시 열면 화면 제어를 해제합니다.

앱 관리형 보조 서비스는 `SMAppService`로 번들 내부 LaunchDaemon을 등록합니다. ad-hoc 서명은 Mac에 따라 서비스 실행이 차단될 수 있습니다. 별도 PKG 경로는 root 소유 LaunchDaemon을 설치합니다. 초기 macOS 승인 이후 비밀번호를 반복 입력하지 않고 조작할 수 있습니다. 아래 복구·서명 규칙은 보조 서비스 모드에 해당합니다.

- XPC 양방향 서명 요구 사항 검증. helper는 현재 콘솔 사용자만 허용합니다. ad-hoc 빌드도 정확한 designated requirement를 사용하며 식별자만으로 허용하는 우회 경로가 없습니다.
- privileged API에는 시작·종료·상태·heartbeat만 있습니다. 임의 명령, 경로, 스크립트를 전달할 수 없습니다.
- root helper가 변경 전 복구 기록을 소유자 root, 디렉터리 0700 / 기록 0600으로 저장합니다.
- 한 XPC 연결만 세션을 소유합니다. 연결 종료 시 복구합니다. 앱이 멈추면 35초 lease + 최대 5초 watchdog 간격 이내에 복구합니다.
- helper는 launchd에 의해 재시작되며 시작 시 남은 복구 기록을 처리합니다. 복구 실패 시 기록을 보존하고 재시도합니다.
- 사용자 전환은 세션을 중지합니다. 앱 재시작 시 임의로 세션을 다시 켜지 않습니다.

앱/helper를 강제 삭제하거나 비활성화하면 복구가 지연되거나 실행되지 않을 수 있습니다. 정상 삭제는 **설정 → 보조 서비스 제거 → 종료 → 앱을 휴지통으로 이동** 순서입니다. 실행 중인 앱을 교체하는 업데이트도 먼저 세션을 끄고 보조 서비스를 제거하세요. 비상 복구:

```sh
sudo /usr/bin/pmset -a disablesleep 0
```

## 로컬 빌드

필수: macOS, Xcode의 Swift 컴파일러와 Command Line Tools. 앱의 최소 OS는 macOS 13입니다.

```sh
./Scripts/test.sh
./Scripts/build.sh
python3 Scripts/test-installation.py
./Scripts/package.sh
open 'dist/pika.app'
```

`dist/pika.app`, `dist/pika-1.0.4.dmg`, `dist/pika-1.0.4.zip`이 생성됩니다. arm64와 x86_64를 모두 포함합니다. 빌드 스크립트는 기본적으로 로컬 ad-hoc 서명을 합니다. ad-hoc 빌드는 앱과 보조 서비스를 함께 설치하는 `.pkg`가 필요합니다. 정식 서명 빌드에서 덮개 닫힘 모드를 쓰려면 앱을 `/Applications`에 설치하고 macOS에서 helper를 승인해야 합니다.

자동 테스트는 fake power driver로 소유권, lease 만료, crash 복구, 실패 rollback, 안전 기준 및 상태 전환을 검증합니다. UI의 초 단위 시계·유휴 센서 조회는 없으며 세션 또는 복구가 진행 중일 때만 10초 heartbeat 타이머가 실행됩니다. 타이머는 메뉴를 펼친 동안에도 동작합니다. 실제 시스템 전원 설정은 바꾸지 않습니다. 수동 실기기 검증 목록은 [QA.md](QA.md)를 참고하세요.

설치된 보조 서비스의 연결만 확인하려면 `'/Applications/pika.app/Contents/MacOS/AlwaysAwake' --check-service`를 실행합니다. `--test-session`은 기존 세션이 없을 때 실제 Session을 켰다가 즉시 끄므로 수동 검증에만 사용합니다. 두 명령은 화면 설정을 바꾸지 않습니다.

ad-hoc 업데이트 후 기존 서비스가 연결되지 않으면 세션 OFF·앱 종료 후 동일 실행 파일의 `--repair-service`로 기존 등록을 갱신할 수 있습니다. macOS 승인이 필요할 수 있습니다. 제거 직후 재등록을 거절하면 잠시 뒤 같은 명령을 다시 실행하세요.

## 정식 웹 배포

```sh
SIGNING_IDENTITY='Developer ID Application: YOUR NAME (TEAMID)' ./Scripts/build.sh
./Scripts/notarize.sh YOUR_KEYCHAIN_PROFILE
```

Apple Developer 계정의 Developer ID 인증서 및 이미 설정한 `notarytool` 키체인 프로필이 필요합니다. 비밀 키·인증서·토큰을 저장소에 넣지 마세요. `notarize.sh`는 앱 공증·staple 후 DMG를 만들고 DMG까지 공증·staple합니다. 웹 다운로드의 서명 여부와 보조 서비스 설치 요구사항은 릴리스에 명시합니다. macOS 보안을 시스템 전체에서 비활성화하지 않습니다.

## 소스 구성

- `Sources/App`: 네이티브 메뉴 막대와 스위치, XPC client, 화면 전원 제어
- `Sources/Helper`: privileged daemon, root 복구 기록, watchdog
- `Sources/Shared`: 전원 세션 상태 기계, 안전 정책, 하드웨어 판독, 서명 검증
- `Tests`: 시스템 설정을 바꾸지 않는 동작 테스트
- `docs`: GitHub Pages 다운로드 페이지
- `Scripts`: Universal 앱 빌드, 아이콘, DMG/ZIP 패키징, 공증

<a id="mcp"></a>

## MCP로 pika 제어

앱에 포함된 네이티브 `pika-mcp` 실행 파일을 STDIO MCP 서버로 등록합니다. Python/Node 설치나 웹 서버는 필요하지 않습니다. 앱과 보조 서비스를 설치한 뒤 `/Applications/pika.app`을 실행하세요.

Codex 설정 예시 (`~/.codex/config.toml`):

```toml
[mcp_servers.pika]
command = "/Applications/pika.app/Contents/MacOS/pika-mcp"
```

등록 후 MCP 서버를 다시 시작합니다. 다른 MCP 클라이언트에서도 같은 실행 파일을 STDIO 방식으로 사용합니다.

| 도구 | 입력 | 동작 |
|---|---|---|
| `pika_status` | 없음 | 앱의 Session/Monitor 설정, 서비스 등록, 배터리·열 상태 조회 |
| `pika_set_session` | `enabled: true/false` | Session을 지정 상태로 설정 |
| `pika_set_monitor` | `enabled: true/false` | Session ON일 때만 화면 유지/잠자기 요청 |

- Session OFF는 Monitor도 OFF로 표시하며 실제 화면을 즉시 끄지는 않습니다.
- 덮개 모드에서는 `waitingForLid: true` 동안 Monitor 선택만 저장합니다. 덮개 닫힘 시 `lidEngaged: true`로 바뀌며 선택을 적용합니다. Monitor OFF는 적용 시점부터 3초 뒤 화면 잠자기를 요청합니다. 반환값은 설정/요청 상태이며 물리 화면 전원 상태를 보장하지 않습니다.
- `serviceRegistered`는 macOS에 등록된 상태입니다. 보조 서비스 연결 성공 여부와 다릅니다. 서명·권한 문제가 있으면 Session 시작이 `isError: true`로 실패합니다.
- MCP 클라이언트 종료는 앱의 세션을 종료하지 않습니다. `pika_set_session(enabled: false)` 또는 앱 스위치로 종료합니다. GUI 앱 종료/heartbeat 유실 시 기존 안전 복구가 적용됩니다.
- MCP는 안전 기준을 변경하거나 임의 명령을 실행하지 않습니다. 현재 사용자 전용 Unix socket을 사용하며 원격 HTTP 접속은 제공하지 않습니다.
- Developer ID 서명이 없는 빌드는 설치형 보조 서비스가 없으면 설치를 안내합니다. MCP의 `sessionMode`, `lidClosedSupported`, `sessionNotice`로 현재 기능 범위를 확인하세요.

프로토콜 검사는 `./Scripts/test.sh`에 포함됩니다. 잘못된 입력/알림은 전원 동작을 실행하지 않으며, 실행 실패는 실제 상태와 함께 반환합니다.

## 관리자 보조 서비스 설치 패키지

`./Scripts/package-helper.sh`는 빌드된 앱으로 `dist/pika-1.0.4.pkg`와 `dist/pika-helper-uninstall-1.0.4.pkg`를 만듭니다. `.pkg`는 앱과 root 소유의 별도 LaunchDaemon을 함께 설치합니다. 앱/보조 서비스 서명은 서로 정확히 일치해야 하므로 서로 다른 빌드의 DMG와 PKG를 섞지 마세요.

설치 전에 Session을 OFF로 하고 기존 앱 관리형 보조 서비스를 제거한 다음 앱을 종료합니다. 이전 버전에서 제거가 안 되면 새 앱의 `--unregister-service` 명령으로 안전 상태를 확인하고 정상 SMAppService API를 통해 제거할 수 있습니다. macOS Installer의 관리자 인증은 사용자가 직접 진행합니다. 설치/제거 스크립트는 복구 기록이나 전원 설정을 임의로 초기화하지 않습니다.

패키지를 만들었다고 덮개 닫힘 동작이 검증되는 것은 아닙니다. 설치 후 `--check-service`, `Scripts/test-mcp-live.py --session`, 실제 덮개 닫힘 중 작업 지속을 확인해야 합니다. 자세한 설치 경로·서명 검증은 [설치 패키지 안내](Resources/Installer/README.md)를 참고하세요.
