# MVP 검증 기록

2026-09-23 / 1.0.0: 21개 정책·복구 테스트 통과. macOS 26.6.2 (Apple Silicon)에서 앱 실행, Monitor 옵션 ON/OFF, 이전 제어창·종료 메뉴 확인.

1.0.1: 메뉴 막대 전용 AppKit UI로 교체. Universal 빌드와 서명 검사, 기존 테스트 21개 통과. 실제 메뉴 막대 프로세스 실행과 네이티브 스위치 렌더링 확인. 실행 파일에서 SwiftUI 의존성 제거 확인. 창이 없는 앱의 메뉴는 현재 UI 자동화 도구가 인식하지 못해 새 메뉴의 실화면 클릭 검증은 별도로 필요합니다. 아래 privileged helper 및 물리적 덮개 닫힘 검증도 아직 완료하지 않았습니다.


2026-09-29 / 1.0.2: 실행 및 재실행 시 작은 제어창 표시, X로 닫아도 동일 프로세스 유지 확인. CUA로 실제 Monitor ON/OFF 및 창 닫기 검증, Lifecycle 로그에서 같은 PID의 열림·닫힘 확인. 상태 막대 항목 생성 로그 확인(상단 아이콘의 실제 화면 클릭은 여전히 미검증). Universal 빌드, 서명 검사, 보호·복구 테스트 21개 통과. 권한을 요구하는 실제 Session ON과 덮개 닫힘 검증은 미완료.


2026-09-29 / 1.0.3: 실제 서비스가 서명 검사 실패로 반복 종료되던 문제 수정. launchd의 상대 argv[0] 대신 dyld 실행 경로로 앱 번들을 찾습니다. 서명된 실제 helper에 절대 경로·상대 경로·파일명 argv[0]을 넣고 cwd=/에서 실행한 검사 3개 통과. 현재 Mac에서 서비스 재등록 후 XPC 연결 성공, 동일 서명 GUI의 --test-session으로 실제 Session ON → OFF 성공, pmset SleepDisabled=0 복구 확인. 보호·복구 테스트 21개 및 Universal 빌드 통과. 메뉴 클릭 후 오류는 즉시 제어창과 경고로 표시하고, XPC 작업 전에 메뉴 tracking을 종료합니다. 이번 검증은 CLI에서 동일 XPC client를 이용했으며 메뉴의 물리적 클릭은 사용자 확인 대상입니다. 실제 덮개 닫힘 테스트는 아직 미완료입니다.

## 자동 검증 범위

`Scripts/test.sh`는 실제 시스템 설정을 바꾸지 않습니다. 다음 시나리오를 fake driver로 검사합니다.

- Session ON/OFF, crash disconnect, helper 재시작, 35초 lease 만료
- 다른 세션/도구의 설정 소유권 보존
- 복구 기록 저장 실패, 전원 변경 실패, OS가 변경을 무시하는 경우
- 복구 실패 시 기록 보존 및 재시도, 외부 설정 변경 감지
- 배터리 경계값 25%/15%, 열 상태 serious/critical, Desktop 모드 조건
- 외장 화면 분리 시 강화된 보호, 배터리 정보 누락 시 보수적 거절

## 실기기 확인 (출시 전)

아래 항목은 직접 확인한 후 체크합니다. 빌드 성공으로 완료 처리하지 않습니다.

- [x] Applications에 설치 후 SMAppService 승인 → XPC 연결 (현재 Mac)
- [ ] 메뉴 막대 클릭 → Session / Monitor 스위치, Option+클릭 → Session 즉시 전환
- [ ] 메뉴를 40초 이상 펼쳐도 세션 heartbeat 유지
- [x] Session ON/OFF 실제 XPC 시작·종료 및 OFF 후 SleepDisabled 0 확인 (드라이버가 ON 변경값도 검증)
- [ ] Monitor ON: display assertion 유지 / OFF: 실제 화면만 잠자기
- [ ] 외장 화면·충전기 없이 덮개를 2분 이상 닫아도 테스트 프로세스의 heartbeat 연속 기록
- [ ] 충전기 연결/분리, 외장 화면 연결/분리 시 UI와 helper의 보호 상태 일치
- [ ] GUI 강제 종료 → SleepDisabled 0 복구
- [ ] GUI SIGSTOP → 약 40초 이내 자동 복구
- [ ] helper 강제 종료 → launchd 재시작 및 복구
- [ ] 사용자 전환 및 로그아웃 시 복구
- [ ] 강제 재시작 후 기록 복구, Session 자동 재시작 없음
- [ ] 보조 서비스 제거 후 재등록
- [ ] Apple Silicon / Intel 각각 실제 실행 및 덮개 동작
- [ ] 정식 Developer ID 서명, Apple 공증, 새 Mac의 Gatekeeper 설치

배터리를 실제로 완전 방전시키거나 Mac을 의도적으로 과열시키지 마세요. 경계 조건은 정책 테스트로 검증하고, 전원 연결·외장 화면 변경은 정상 환경에서 확인합니다. 가방 속 테스트는 하지 않습니다.
