Source: https://no-sleep-pika.online/guide/ko/
Language: ko

[← 홈](https://no-sleep-pika.online/ko/)

# 맥북 덮개를 닫고 작업하기: pika 사용 가이드

Session으로 작업을 유지하고, Monitor로 덮개를 닫은 뒤의 화면 동작을 선택하세요.

2026년 10월 1일 업데이트

[맥북 덮어도 안꺼지게 하는법 →](https://no-sleep-pika.online/guide/ko/macbook-lid-closed/)

## 덮개를 닫고 세션 시작하기

통합 pika PKG를 설치한 뒤 /Applications/pika.app을 여세요. 보조 서비스 연결을 확인하고 Session ON → Monitor 선택 → 맥북 덮개 닫기 순서로 사용하세요. 통풍을 확보해 주세요.

Session ON만으로 화면을 즉시 끄거나 잠그지 않습니다. 덮개가 열려 있을 때 Monitor를 바꾸면 선택만 저장하고, 덮개를 닫은 뒤 화면 설정을 적용합니다. 다시 열면 예약된 화면 끄기를 취소합니다.

작업이 끝나면 Session을 OFF로 바꾸세요. pika가 관리하던 잠자기 설정을 복구하고 Monitor 표시도 OFF로 바뀝니다. 화면을 즉시 끄지는 않습니다. 제어창만 닫으면 pika는 메뉴 막대에서 계속 실행됩니다.

## Monitor OFF 상태에서 잠금 화면이 뜨면 절전인가요?

화면 잠금과 시스템 잠자기는 서로 다른 상태입니다. Monitor OFF는 덮개를 닫은 뒤 화면 잠자기를 요청하며, macOS의 잠금 화면 설정에 따라 암호 입력이 필요할 수 있습니다. pika 때문에 암호 요구 설정을 해제할 필요는 없습니다.

Session과 보조 서비스가 활성 상태인 동안 pika는 Mac이 깨어 있도록 요청합니다. 잠금 화면이 보인다는 이유만으로 백그라운드 작업이 멈췄다고 판단할 수는 없습니다. 다만 개별 앱이 잠금 중 작업을 멈추거나 입력을 기다릴 수 있으므로 실제 Agent나 작업 로그를 확인하세요.

배터리·열 보호 기준에 도달하거나 보조 서비스 연결이 끊기거나 앱이 응답하지 않으면 세션이 종료될 수 있습니다. Session ON이 작업의 무제한 실행을 보장하지는 않습니다.

## 네트워크나 AI Agent 연결이 끊길 수도 있나요?

네. 시스템 잠자기를 막아도 네트워크 연결을 보장하지는 않습니다. Wi-Fi 신호, 공유기·통신사 장애, VPN 정책, 원격 API의 시간 초과나 사용량 제한으로 작업이 끊길 수 있습니다. pika는 Wi-Fi 재연결이나 Agent 요청 재시도를 수행하지 않습니다.

처음에는 짧은 작업으로 덮개를 닫았다가 열어 보고, 해당 작업 로그의 시간과 오류를 확인하세요. 작업이 멈췄다면 pika 세션 상태와 네트워크를 함께 점검하세요. 로컬 프로세스는 실행 중이어도 외부 API 요청은 실패할 수 있습니다.

Wi-Fi 문제는 Option 키를 누른 채 Wi-Fi 메뉴를 클릭해 무선 진단을 여세요. 장시간 원격 작업에는 Agent가 제공하는 재시도와 중간 저장 기능을 함께 사용하세요.

## 앱 안에서 업데이트하기

이전 버전에서 업데이트 조회가 실패하거나 macOS가 pika-updater를 차단하면, 통합 PKG로 1.0.13 이상을 한 번 설치하세요. 그 이후에는 메뉴 막대의 업데이트 확인… 또는 제어창의 업데이트…에서 진행할 수 있습니다. 자동 확인은 메뉴에 새 버전을 표시하며, 설치는 사용자가 시작합니다.

덮개를 열고 작업을 마친 뒤 업데이트하세요. Session을 종료하고 파일을 검증한 다음 macOS 기본 설치 프로그램을 엽니다. 승인과 설치를 마친 뒤 응용 프로그램에서 pika를 다시 여세요. PKG는 앱과 보조 서비스를 함께 교체하며 Session은 OFF로 유지됩니다. 설치를 취소했다면 pika를 다시 열어 재시도할 수 있습니다. 업데이트 후 MCP 클라이언트 연결도 다시 시작하세요.

## 메뉴 막대 아이콘이 보이지 않을 때

응용 프로그램에서 pika를 열면 제어창이 전면에 나타납니다. 이 창을 닫아도 앱은 계속 실행됩니다. 아이콘이 많아 메뉴 막대가 붐비면 다른 메뉴 막대 항목을 줄이거나 메뉴가 적은 앱으로 전환한 뒤 다시 확인하세요.

여러 번 실행하기 전에 활성 상태 보기에서 pika / AlwaysAwake가 실행 중인지 확인하세요. 완전히 종료하려면 창의 × 대신 pika의 종료 기능을 사용하세요.

## 로컬 MCP 클라이언트에 pika 연결하기

MCP 클라이언트와 같은 Mac·사용자 계정에서 pika를 실행해 두세요. Mac 내부의 STDIO 방식이며 홈페이지 주소는 MCP 서버 주소가 아닙니다.

Codex CLI가 설치되어 있다면 터미널에서 한 번 실행하세요:

```
codex mcp add pika -- /Applications/pika.app/Contents/MacOS/pika-mcp
```

또는 ~/.codex/config.toml에 아래 설정을 넣으세요. pika 항목이 이미 있으면 중복 추가하지 말고 수정하세요:

```
[mcp_servers.pika]
command = "/Applications/pika.app/Contents/MacOS/pika-mcp"
```

MCP 클라이언트를 재시작하고 새 대화에서 “pika_status를 호출해 상태를 알려줘. Session이나 Monitor는 변경하지 마”라고 요청하세요. 도구가 정상 응답하면 앱 연결이 확인됩니다. 제어를 요청하기 전에 sessionOn, recoveryRequired, lastError를 확인하세요.

pika_set_session은 Session을 제어합니다. pika_set_monitor는 Monitor를 제어하며 Session ON이 필요합니다. 다른 로컬 MCP 클라이언트에서는 STDIO를 선택하고 아래 실행 경로를 넣으세요. 인수와 API 키는 필요 없습니다:

```
/Applications/pika.app/Contents/MacOS/pika-mcp
```

Agent를 종료해도 pika 세션은 유지됩니다. 앱에서 Session을 끄거나 Agent에게 종료를 요청하세요.

## 설치 또는 보조 서비스 연결이 실패했나요?

설치 안내에서 통합 PKG 사용, macOS 보안 경고, pika 종료 후 재설치 방법을 확인하세요. 현재 다운로드는 Developer ID 서명·공증이 없으며 macOS 보안 설정에 따라 동작이 달라질 수 있습니다.

[pika 설치 안내 →](https://no-sleep-pika.online/install/ko/)
