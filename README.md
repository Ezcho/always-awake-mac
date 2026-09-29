# Always Awake

macOS 메뉴 막대에서 Session과 Monitor를 제어하는 네이티브 앱입니다. Swift / AppKit으로 만들었으며 외부 패키지나 서버 없이 실행됩니다.

[다운로드 페이지](https://ezcho.github.io/always-awake-mac/) · [MVP 다운로드](https://github.com/Ezcho/always-awake-mac/releases/tag/v1.0.2-mvp)

> **MVP 테스트 빌드** — Developer ID 서명·Apple 공증 전입니다. 자동 테스트와 빌드 검증은 실제 덮개 닫힘·과열·방전 실기기 검증을 대체하지 않습니다. macOS의 `disablesleep` 설정은 비공개 동작에 의존하므로 OS 업데이트 후 다시 검증해야 합니다.

## 사용

1. DMG를 열고 **Always Awake.app**을 **Applications**로 드래그합니다.
2. 앱을 실행하고 메뉴 막대의 **권한 허용…**를 누릅니다.
3. macOS **시스템 설정 → 일반 → 로그인 항목 및 확장 프로그램**에서 Always Awake를 승인합니다. 관리자 승인이 필요할 수 있습니다.
4. **Session ON**으로 잠자기를 차단합니다. **Monitor OFF**는 3초 후 화면만 끕니다.

메뉴 막대 아이콘 **클릭**으로 Session·Monitor 스위치를 엽니다. **Option+클릭**은 Session을 바로 전환합니다. 실행하면 작은 제어창이 표시됩니다. 창의 X를 눌러 닫아도 Session과 메뉴 막대는 유지됩니다. 앱을 다시 실행하거나 메뉴의 **제어창 열기**로 창을 다시 엽니다. Dock 아이콘은 없습니다. 종료는 메뉴의 **종료**를 사용합니다.

- Monitor ON: 세션 동안 화면의 자동 잠자기를 막습니다. 덮개가 닫힌 내장 화면은 켜지지 않습니다.
- Monitor OFF: 세션 중 화면을 잠자기로 보냅니다. 키보드·마우스로 다시 켤 수 있습니다. 화면 잠금은 별도입니다.
- Session OFF / 정상 종료: 이 앱이 변경한 시스템 잠자기 설정과 화면 assertion을 해제합니다.
- 다른 앱이 이미 `SleepDisabled=1`을 설정했다면 시작을 거절하여 기존 소유권을 보존합니다.
- 네트워크, AI 서비스 제한, 브라우저 백그라운드 정책, 에이전트 자체 오류·종료는 관리하지 않습니다.

## 과열·방전 보호

5초마다 실제 전원·배터리·덮개·외장 화면·macOS 열 상태를 확인합니다. 별도의 복잡한 설정 없이 아래 기준으로 자동 전환합니다. 배터리 기준은 외부 전원 없이 사용할 때 적용합니다.

| 사용 상태 | 배터리 기준 | macOS 열 상태 기준 |
| --- | --- | --- |
| 덮개 닫힘 + 외장 화면 없음 | 25% 이하 | serious(높음) 이상 |
| 일반 사용 / 배터리로 외장 화면 사용 | 15% 이하 | critical(위험) |
| Desktop: 외부 전원 + 외장 화면 | 해당 없음 | critical(위험) |

안전 기준에 도달하면 Session을 해제하고 **Mac 전체를 잠자기로 전환**합니다. 작업 프로세스를 강제로 종료하지 않지만 작업을 자동 저장하는 기능은 아닙니다. 안전 중단 후 세션을 자동 재개하지 않습니다. 열 상태는 섭씨 센서값이 아닌 macOS의 thermal pressure입니다. 가방 안 사용의 안전을 보장하지 않으며, 통풍이 되는 곳에서 사용해야 합니다.

## 구조와 복구

앱은 `SMAppService`로 번들 내부 LaunchDaemon을 등록합니다. 초기 macOS 승인 이후 비밀번호를 반복 입력하지 않고 조작할 수 있습니다.

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
./Scripts/package.sh
open 'dist/Always Awake.app'
```

`dist/Always Awake.app`, `dist/Always-Awake-1.0.2.dmg`, `dist/Always-Awake-1.0.2.zip`이 생성됩니다. arm64와 x86_64를 모두 포함합니다. 빌드 스크립트는 기본적으로 로컬 ad-hoc 서명을 합니다. 앱은 `/Applications`에 설치된 뒤 helper 등록을 허용합니다. 실제 보호 기능을 테스트하려면 macOS에서 helper를 직접 승인해야 합니다.

자동 테스트는 fake power driver로 소유권, lease 만료, crash 복구, 실패 rollback, 안전 기준 및 상태 전환을 검증합니다. UI의 초 단위 시계·유휴 센서 조회는 없으며 세션 또는 복구가 진행 중일 때만 10초 heartbeat 타이머가 실행됩니다. 타이머는 메뉴를 펼친 동안에도 동작합니다. 실제 시스템 전원 설정은 바꾸지 않습니다. 수동 실기기 검증 목록은 [QA.md](QA.md)를 참고하세요.

## 정식 웹 배포

```sh
SIGNING_IDENTITY='Developer ID Application: YOUR NAME (TEAMID)' ./Scripts/build.sh
./Scripts/notarize.sh YOUR_KEYCHAIN_PROFILE
```

Apple Developer 계정의 Developer ID 인증서 및 이미 설정한 `notarytool` 키체인 프로필이 필요합니다. 비밀 키·인증서·토큰을 저장소에 넣지 마세요. `notarize.sh`는 앱 공증·staple 후 DMG를 만들고 DMG까지 공증·staple합니다. 정식 서명 전 MVP는 GitHub prerelease로 구분합니다. macOS 보안을 시스템 전체에서 비활성화하지 않습니다.

## 소스 구성

- `Sources/App`: 네이티브 메뉴 막대와 스위치, XPC client, 화면 전원 제어
- `Sources/Helper`: privileged daemon, root 복구 기록, watchdog
- `Sources/Shared`: 전원 세션 상태 기계, 안전 정책, 하드웨어 판독, 서명 검증
- `Tests`: 시스템 설정을 바꾸지 않는 동작 테스트
- `docs`: GitHub Pages 다운로드 페이지
- `Scripts`: Universal 앱 빌드, 아이콘, DMG/ZIP 패키징, 공증
