# MVP 검증 기록

2026-09-23 로컬 검증: 21개 정책·복구 테스트 통과. macOS 26.6.2 (Apple Silicon)에서 앱 실행, Monitor 옵션 ON/OFF, 제어창·종료 메뉴 확인. arm64/x86_64 Universal 빌드, ad-hoc 서명 무결성 검사, DMG/ZIP 생성 확인. 아래 privileged helper 및 물리적 덮개 닫힘 검증은 아직 완료하지 않았습니다.

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

- [ ] Applications에 설치 후 SMAppService 승인 → XPC 연결
- [ ] Session ON: `pmset -g`에서 SleepDisabled 1 / OFF: 0
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
