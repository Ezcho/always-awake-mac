Source: https://no-sleep-pika.online/ko/
Language: ko

# 맥을 덮어도 작업을 유지하세요

[Mac용 다운로드](https://github.com/Ezcho/always-awake-mac/releases/download/v1.0.13/pika-1.0.13.pkg) 

36 다운로드

공개 버전 1.0.13 · macOS 13+ · Apple Silicon 및 Intel

## MCP 연결

STDIO

pika를 설치하고 실행한 뒤 아래 명령어로 연결하세요. [소스코드 보기 ↗](https://github.com/Ezcho/always-awake-mac#mcp)

`/Applications/pika.app/Contents/MacOS/pika-mcp`

## AI Agent에 pika 연결하기

같은 Mac에서 한 번만 설정하면, Agent가 상태를 확인하고 Session / Monitor를 제어할 수 있어요.

### 1pika 먼저 준비하기

pika PKG로 앱과 보조 서비스를 함께 설치하세요. 응용 프로그램에서 pika를 열고 메뉴 막대에서 실행 중인 상태로 두세요. [설치 도움말 ↗](https://no-sleep-pika.online/install/ko/)

### 2MCP 서버 등록하기

Codex CLI가 설치되어 있다면 터미널에 아래 명령을 한 번 실행하세요. 연결할 때 MCP 클라이언트가 서버를 실행합니다.

`codex mcp add pika -- /Applications/pika.app/Contents/MacOS/pika-mcp`

Codex CLI가 없나요? 설정 파일로 연결

Codex의 ~/.codex/config.toml 파일에 아래 항목을 추가하세요. pika 항목이 이미 있으면 해당 항목만 수정하고, 다른 설정은 유지하세요.

```
[mcp_servers.pika]
command = "/Applications/pika.app/Contents/MacOS/pika-mcp"
```

다른 로컬 MCP 클라이언트

MCP 서버 추가에서 이름은 pika, 연결 방식은 STDIO로 선택하세요. Command에 아래 경로를 넣고, 인수와 환경변수는 비워 두세요. 서버 URL이나 API 키는 필요하지 않습니다.

`/Applications/pika.app/Contents/MacOS/pika-mcp`

이 연결은 Mac 내부의 STDIO 방식입니다. 홈페이지 주소는 MCP 서버 주소가 아니며, URL만 받는 클라우드 연결에는 이 실행 파일을 등록할 수 없습니다.

[Codex 공식 문서 ↗](https://learn.chatgpt.com/docs/extend/mcp?surface=cli) 

### 3연결 확인하기

저장 후 MCP 클라이언트를 재시작하고 새 대화에서 이렇게 요청하세요.

`pika_status를 호출해서 현재 상태를 알려줘. Session과 Monitor는 변경하지 마.`

pika_status 도구가 상태를 정상 반환하면 앱 연결이 확인된 것입니다. Session이 OFF여도 정상이며, 서비스 등록만으로 보조 서비스 연결까지 확인되는 것은 아닙니다.

### 연결 후 사용할 도구

`pika_set_session` — Session 켜기 / 끄기
`pika_set_monitor` — Monitor 켜기 / 끄기 · Session ON 필요

Session ON은 준비 상태입니다. 덮개를 닫아야 화면 설정이 적용되고, 덮개가 열려 있을 때 Monitor 변경은 선택만 저장합니다.

Agent를 종료해도 pika 세션은 유지됩니다. 종료할 때는 앱에서 Session을 끄거나 Agent에게 꺼 달라고 요청하세요.

연결이 안 될 때

도구가 안 보이면 실행 경로를 확인하고 클라이언트를 재시작하세요. 앱 연결 오류라면 같은 Mac·사용자 계정에서 pika를 실행하세요. 보조 서비스 오류라면 pika를 종료하고 최신 통합 PKG를 다시 설치한 뒤 여세요. 터미널에서 codex 명령을 찾지 못하면 위의 설정 파일 방식을 사용하세요.
