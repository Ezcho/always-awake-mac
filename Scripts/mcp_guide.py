"""Compact MCP setup overlay; commands are data, never executed by the website."""
from html import escape

COMMAND = '/Applications/pika.app/Contents/MacOS/pika-mcp'
LABELS = {
    'en': 'Connection guide', 'ko': '연결 방법 자세히', 'zh-CN': '连接指南 · English',
    'zh-TW': '連線指南 · English', 'ja': '接続ガイド · English', 'hi': 'कनेक्शन गाइड · English',
    'id': 'Panduan koneksi · English', 'es': 'Guía de conexión · English',
    'fr': 'Guide de connexion · English', 'de': 'Verbindungsanleitung · English',
    'pt-BR': 'Guia de conexão · English', 'ru': 'Подключение · English',
    'ar': 'دليل الاتصال · English', 'vi': 'Hướng dẫn kết nối · English', 'th': 'วิธีเชื่อมต่อ · English'
}
TEXT = {
'en': {
    'title': 'Connect your agent to pika', 'close': 'Close',
    'intro': 'Set up once on the same Mac. Your agent can then read status and control Session / Monitor.',
    'prepare': 'Prepare pika',
    'preparebody': 'Install the pika PKG, which includes the app and helper. Open pika from Applications and keep it running in the menu bar.',
    'install': 'Installation help', 'register': 'Add the MCP server',
    'registerbody': 'If Codex CLI is installed, paste this into Terminal once. The MCP client starts the server when it connects.',
    'manual': 'No Codex CLI? Use a configuration file',
    'manualbody': 'For Codex, add this section to ~/.codex/config.toml. If pika already exists, update it instead of adding a duplicate. Keep your other settings.',
    'other': 'Other local MCP clients',
    'otherbody': 'Add a server named pika using STDIO. Set Command to the path below. Leave arguments and environment variables empty. No server URL or API key is required.',
    'verify': 'Check the connection',
    'verifybody': 'Save, restart your MCP client, and open a new chat. Ask your agent:',
    'prompt': 'Call pika_status and show the current state. Do not change Session or Monitor.',
    'success': 'A successful pika_status tool result confirms the connection to the app. Session OFF is normal; helper registration alone does not confirm helper connectivity.',
    'tools': 'What you can ask next',
    'session': 'Session ON / OFF', 'monitor': 'Monitor ON / OFF · requires Session ON',
    'lid': 'Session ON prepares pika. Display policy applies only after the lid closes. With the lid open, Monitor changes only save your preference.',
    'stop': 'Closing the agent does not end a pika session. Turn Session OFF in pika or ask your agent to do so.',
    'trouble': 'Connection not working?',
    'troublebody': 'No tools: confirm the command path and restart the client. App connection error: open pika on the same Mac and user account. Helper error: quit pika, reinstall the latest full PKG, and reopen pika. If Terminal says codex was not found, use the configuration-file option above.',
    'local': 'This is a local STDIO connection. The website address is not an MCP endpoint, and a cloud-only URL connector cannot run this Mac executable.',
    'official': 'Codex official documentation',
},
'ko': {
    'title': 'AI Agent에 pika 연결하기', 'close': '닫기',
    'intro': '같은 Mac에서 한 번만 설정하면, Agent가 상태를 확인하고 Session / Monitor를 제어할 수 있어요.',
    'prepare': 'pika 먼저 준비하기',
    'preparebody': 'pika PKG로 앱과 보조 서비스를 함께 설치하세요. 응용 프로그램에서 pika를 열고 메뉴 막대에서 실행 중인 상태로 두세요.',
    'install': '설치 도움말', 'register': 'MCP 서버 등록하기',
    'registerbody': 'Codex CLI가 설치되어 있다면 터미널에 아래 명령을 한 번 실행하세요. 연결할 때 MCP 클라이언트가 서버를 실행합니다.',
    'manual': 'Codex CLI가 없나요? 설정 파일로 연결',
    'manualbody': 'Codex의 ~/.codex/config.toml 파일에 아래 항목을 추가하세요. pika 항목이 이미 있으면 해당 항목만 수정하고, 다른 설정은 유지하세요.',
    'other': '다른 로컬 MCP 클라이언트',
    'otherbody': 'MCP 서버 추가에서 이름은 pika, 연결 방식은 STDIO로 선택하세요. Command에 아래 경로를 넣고, 인수와 환경변수는 비워 두세요. 서버 URL이나 API 키는 필요하지 않습니다.',
    'verify': '연결 확인하기',
    'verifybody': '저장 후 MCP 클라이언트를 재시작하고 새 대화에서 이렇게 요청하세요.',
    'prompt': 'pika_status를 호출해서 현재 상태를 알려줘. Session과 Monitor는 변경하지 마.',
    'success': 'pika_status 도구가 상태를 정상 반환하면 앱 연결이 확인된 것입니다. Session이 OFF여도 정상이며, 서비스 등록만으로 보조 서비스 연결까지 확인되는 것은 아닙니다.',
    'tools': '연결 후 사용할 도구',
    'session': 'Session 켜기 / 끄기', 'monitor': 'Monitor 켜기 / 끄기 · Session ON 필요',
    'lid': 'Session ON은 준비 상태입니다. 덮개를 닫아야 화면 설정이 적용되고, 덮개가 열려 있을 때 Monitor 변경은 선택만 저장합니다.',
    'stop': 'Agent를 종료해도 pika 세션은 유지됩니다. 종료할 때는 앱에서 Session을 끄거나 Agent에게 꺼 달라고 요청하세요.',
    'trouble': '연결이 안 될 때',
    'troublebody': '도구가 안 보이면 실행 경로를 확인하고 클라이언트를 재시작하세요. 앱 연결 오류라면 같은 Mac·사용자 계정에서 pika를 실행하세요. 보조 서비스 오류라면 pika를 종료하고 최신 통합 PKG를 다시 설치한 뒤 여세요. 터미널에서 codex 명령을 찾지 못하면 위의 설정 파일 방식을 사용하세요.',
    'local': '이 연결은 Mac 내부의 STDIO 방식입니다. 홈페이지 주소는 MCP 서버 주소가 아니며, URL만 받는 클라우드 연결에는 이 실행 파일을 등록할 수 없습니다.',
    'official': 'Codex 공식 문서',
}}


def render(locale, copy, copied, copyfail):
    language = 'ko' if locale == 'ko' else 'en'
    t = TEXT[language]
    h = lambda key: escape(t[key])
    def block(identifier, value):
        return f'''<div class="terminal-body"><div class="command" dir="ltr"><code id="{identifier}">{escape(value)}</code><button type="button" class="copy" data-copy="{identifier}" data-copied="{escape(copied)}" data-failed="{escape(copyfail)}">{escape(copy)}</button></div><span class="copy-status sr-only" role="status" aria-live="polite"></span></div>'''
    return f'''<button type="button" class="mcp-guide-open" data-open-mcp aria-haspopup="dialog">{escape(LABELS[locale])} <span aria-hidden="true">↗</span></button>
<dialog class="mcp-guide" id="mcp-guide" aria-labelledby="mcp-guide-title" lang="{language}" dir="ltr">
<div class="guide-header"><h2 id="mcp-guide-title">{h('title')}</h2><form method="dialog"><button class="guide-close" aria-label="{h('close')}" autofocus>×</button></form></div>
<p class="guide-intro">{h('intro')}</p>
<div class="guide-grid"><section class="guide-prepare"><h3><span>1</span>{h('prepare')}</h3><p>{h('preparebody')} <a href="/install/{'ko/' if language == 'ko' else ''}">{h('install')} ↗</a></p></section>
<section class="guide-register"><h3><span>2</span>{h('register')}</h3><p>{h('registerbody')}</p>{block('mcp-codex-add', 'codex mcp add pika -- ' + COMMAND)}
<details open><summary>{h('manual')}</summary><p>{h('manualbody')}</p>{block('mcp-codex-config', '[mcp_servers.pika]\ncommand = "' + COMMAND + '"')}</details>
<details><summary>{h('other')}</summary><p>{h('otherbody')}</p>{block('mcp-stdio-path', COMMAND)}</details>
<p class="guide-hint">{h('local')}</p><a class="guide-source" href="https://learn.chatgpt.com/docs/extend/mcp?surface=cli">{h('official')} ↗</a>
</section>
<section class="guide-verify"><h3><span>3</span>{h('verify')}</h3><p>{h('verifybody')}</p>{block('mcp-status-prompt', t['prompt'])}<p class="guide-hint">{h('success')}</p></section>
<section class="guide-tools"><h3>{h('tools')}</h3><p><code>pika_set_session</code> — {h('session')}<br><code>pika_set_monitor</code> — {h('monitor')}</p><p>{h('lid')}</p><p>{h('stop')}</p></section></div>
<details class="guide-trouble"><summary>{h('trouble')}</summary><p>{h('troublebody')}</p></details>
</dialog>'''
