"""Useful, indexable product documentation; no JavaScript is needed to read it."""
import html
import json

UPDATED = '2026-09-30'  # Change only when this guide's content changes.
COMMAND = '/Applications/pika.app/Contents/MacOS/pika-mcp'
COPY = {
    'en': {
        'title': 'Keep a MacBook awake with the lid closed: pika guide',
        'description': 'How pika Session and Monitor work with a closed MacBook lid, what a locked screen means, Wi-Fi limits, and local MCP setup for AI agents.',
        'home': 'Home', 'install': 'Install pika', 'language': 'Guide language',
        'intro': 'Use Session to keep work running, and Monitor to choose the display behavior after you close the lid.',
        'updated': 'Updated September 30, 2026',
        'sections': [
            ('start', 'Start a closed-lid session', [
                'Install the full pika PKG and open /Applications/pika.app. Wait for the helper connection, turn Session ON, choose Monitor, then close your MacBook’s lid. Keep the Mac ventilated.',
                'Turning Session ON does not immediately blank or lock the screen. While the lid is open, changing Monitor saves your choice; pika applies its display policy after the lid closes. Reopening the lid cancels pending display-off work.',
                'When you finish, turn Session OFF. This restores the sleep setting managed by pika and shows Monitor as OFF. It does not immediately turn off the screen. Closing the control window keeps pika running in the menu bar.'
            ]),
            ('lock', 'Monitor OFF, screen locked: is the Mac asleep?', [
                'A locked screen and system sleep are different states. Monitor OFF requests display sleep after the lid closes; macOS may then require your password according to your Lock Screen settings. You do not need to disable that password requirement for pika.',
                'While the Session and helper remain active, pika requests that the Mac stay awake. A lock screen alone does not prove that background work has stopped. An individual app may still pause when locked or need user input; check your actual agent or job log.',
                'pika can end a session when battery or thermal protection triggers, the helper connection is lost, or the app stops responding. Session ON is not a promise that a job will run indefinitely.'
            ]),
            ('network', 'Can Wi-Fi or an AI agent disconnect?', [
                'Yes. Preventing system sleep does not guarantee a network connection. Wi-Fi signal, router or ISP outages, VPN policies, and a remote API’s timeout or service limits can still interrupt a job. pika does not reconnect Wi-Fi or retry your agent’s failed requests.',
                'For a first run, try a short job with the lid closed, reopen the Mac, and check timestamps and errors in the job’s own log. If work stopped, check both pika’s session status and the network. A local process can continue while a remote API request fails.',
                'For Wi-Fi problems, Option-click the Wi-Fi menu and open Wireless Diagnostics. For long remote jobs, use the agent’s supported retry and checkpoint features when available.'
            ]),
            ('menu', 'The menu bar icon is missing', [
                'Open pika from Applications to bring its controls to the foreground. Closing that window leaves the app running. If many status items crowd the menu bar, reduce other menu bar items or switch to an app with fewer menus, then check again.',
                'Check Activity Monitor for pika / AlwaysAwake before opening more copies. To quit fully, use pika’s Quit action rather than the window’s × button.'
            ]),
        ],
        'mcp': 'Connect pika to a local MCP client',
        'mcp_intro': 'Keep pika running on the same Mac and user account as your MCP client. The server uses local STDIO; the website address is not an MCP endpoint.',
        'mcp_cli': 'With Codex CLI installed, run once in Terminal:',
        'mcp_manual': 'Or add this to ~/.codex/config.toml. Update an existing pika entry instead of duplicating it:',
        'mcp_check': 'Restart the MCP client and open a new chat. Ask: “Call pika_status and show the state without changing Session or Monitor.” A successful tool response confirms the app connection. Inspect sessionOn, recoveryRequired and lastError before requesting changes.',
        'mcp_tools': 'pika_set_session controls Session. pika_set_monitor controls Monitor and requires Session ON. For another local MCP client, use STDIO with the executable path below, no arguments, and no API key:',
        'mcp_stop': 'Closing the agent does not end the pika session. Turn Session OFF in the app or ask the agent to do it.',
        'help': 'Installation or helper connection failed?',
        'help_body': 'The installation guide covers the unified PKG, macOS security warnings, and reinstalling after quitting pika. The download is not Developer ID signed or notarized; behavior depends on macOS security settings.',
        'source': 'Source code and issue tracker', 'apple': 'Apple Wi-Fi troubleshooting',
    },
    'ko': {
        'title': '맥북 덮개를 닫고 작업하기: pika 사용 가이드',
        'description': '맥북 덮개를 닫았을 때 pika Session·Monitor 동작, 화면 잠금과 절전의 차이, Wi-Fi 끊김 가능성과 AI 에이전트 MCP 연결 방법을 안내합니다.',
        'home': '홈', 'install': 'pika 설치 안내', 'language': '안내 언어',
        'intro': 'Session으로 작업을 유지하고, Monitor로 덮개를 닫은 뒤의 화면 동작을 선택하세요.',
        'updated': '2026년 9월 30일 업데이트',
        'sections': [
            ('start', '덮개를 닫고 세션 시작하기', [
                '통합 pika PKG를 설치한 뒤 /Applications/pika.app을 여세요. 보조 서비스 연결을 확인하고 Session ON → Monitor 선택 → 맥북 덮개 닫기 순서로 사용하세요. 통풍을 확보해 주세요.',
                'Session ON만으로 화면을 즉시 끄거나 잠그지 않습니다. 덮개가 열려 있을 때 Monitor를 바꾸면 선택만 저장하고, 덮개를 닫은 뒤 화면 설정을 적용합니다. 다시 열면 예약된 화면 끄기를 취소합니다.',
                '작업이 끝나면 Session을 OFF로 바꾸세요. pika가 관리하던 잠자기 설정을 복구하고 Monitor 표시도 OFF로 바뀝니다. 화면을 즉시 끄지는 않습니다. 제어창만 닫으면 pika는 메뉴 막대에서 계속 실행됩니다.'
            ]),
            ('lock', 'Monitor OFF 상태에서 잠금 화면이 뜨면 절전인가요?', [
                '화면 잠금과 시스템 잠자기는 서로 다른 상태입니다. Monitor OFF는 덮개를 닫은 뒤 화면 잠자기를 요청하며, macOS의 잠금 화면 설정에 따라 암호 입력이 필요할 수 있습니다. pika 때문에 암호 요구 설정을 해제할 필요는 없습니다.',
                'Session과 보조 서비스가 활성 상태인 동안 pika는 Mac이 깨어 있도록 요청합니다. 잠금 화면이 보인다는 이유만으로 백그라운드 작업이 멈췄다고 판단할 수는 없습니다. 다만 개별 앱이 잠금 중 작업을 멈추거나 입력을 기다릴 수 있으므로 실제 Agent나 작업 로그를 확인하세요.',
                '배터리·열 보호 기준에 도달하거나 보조 서비스 연결이 끊기거나 앱이 응답하지 않으면 세션이 종료될 수 있습니다. Session ON이 작업의 무제한 실행을 보장하지는 않습니다.'
            ]),
            ('network', '네트워크나 AI Agent 연결이 끊길 수도 있나요?', [
                '네. 시스템 잠자기를 막아도 네트워크 연결을 보장하지는 않습니다. Wi-Fi 신호, 공유기·통신사 장애, VPN 정책, 원격 API의 시간 초과나 사용량 제한으로 작업이 끊길 수 있습니다. pika는 Wi-Fi 재연결이나 Agent 요청 재시도를 수행하지 않습니다.',
                '처음에는 짧은 작업으로 덮개를 닫았다가 열어 보고, 해당 작업 로그의 시간과 오류를 확인하세요. 작업이 멈췄다면 pika 세션 상태와 네트워크를 함께 점검하세요. 로컬 프로세스는 실행 중이어도 외부 API 요청은 실패할 수 있습니다.',
                'Wi-Fi 문제는 Option 키를 누른 채 Wi-Fi 메뉴를 클릭해 무선 진단을 여세요. 장시간 원격 작업에는 Agent가 제공하는 재시도와 중간 저장 기능을 함께 사용하세요.'
            ]),
            ('menu', '메뉴 막대 아이콘이 보이지 않을 때', [
                '응용 프로그램에서 pika를 열면 제어창이 전면에 나타납니다. 이 창을 닫아도 앱은 계속 실행됩니다. 아이콘이 많아 메뉴 막대가 붐비면 다른 메뉴 막대 항목을 줄이거나 메뉴가 적은 앱으로 전환한 뒤 다시 확인하세요.',
                '여러 번 실행하기 전에 활성 상태 보기에서 pika / AlwaysAwake가 실행 중인지 확인하세요. 완전히 종료하려면 창의 × 대신 pika의 종료 기능을 사용하세요.'
            ]),
        ],
        'mcp': '로컬 MCP 클라이언트에 pika 연결하기',
        'mcp_intro': 'MCP 클라이언트와 같은 Mac·사용자 계정에서 pika를 실행해 두세요. Mac 내부의 STDIO 방식이며 홈페이지 주소는 MCP 서버 주소가 아닙니다.',
        'mcp_cli': 'Codex CLI가 설치되어 있다면 터미널에서 한 번 실행하세요:',
        'mcp_manual': '또는 ~/.codex/config.toml에 아래 설정을 넣으세요. pika 항목이 이미 있으면 중복 추가하지 말고 수정하세요:',
        'mcp_check': 'MCP 클라이언트를 재시작하고 새 대화에서 “pika_status를 호출해 상태를 알려줘. Session이나 Monitor는 변경하지 마”라고 요청하세요. 도구가 정상 응답하면 앱 연결이 확인됩니다. 제어를 요청하기 전에 sessionOn, recoveryRequired, lastError를 확인하세요.',
        'mcp_tools': 'pika_set_session은 Session을 제어합니다. pika_set_monitor는 Monitor를 제어하며 Session ON이 필요합니다. 다른 로컬 MCP 클라이언트에서는 STDIO를 선택하고 아래 실행 경로를 넣으세요. 인수와 API 키는 필요 없습니다:',
        'mcp_stop': 'Agent를 종료해도 pika 세션은 유지됩니다. 앱에서 Session을 끄거나 Agent에게 종료를 요청하세요.',
        'help': '설치 또는 보조 서비스 연결이 실패했나요?',
        'help_body': '설치 안내에서 통합 PKG 사용, macOS 보안 경고, pika 종료 후 재설치 방법을 확인하세요. 현재 다운로드는 Developer ID 서명·공증이 없으며 macOS 보안 설정에 따라 동작이 달라질 수 있습니다.',
        'source': '소스코드와 문제 신고', 'apple': 'Apple Wi-Fi 문제 해결 안내',
    },
}


def render(locale, base, repo):
    t = COPY[locale]
    e = html.escape
    url = base + ('/guide/ko/' if locale == 'ko' else '/guide/')
    home = '/ko/' if locale == 'ko' else '/'
    install = '/install/ko/' if locale == 'ko' else '/install/'
    sections = ''.join(f'<section id="{key}"><h2>{e(title)}</h2>' + ''.join(f'<p>{e(p)}</p>' for p in paragraphs) + '</section>' for key, title, paragraphs in t['sections'])
    contents = ''.join(f'<a href="#{key}">{e(title)}</a>' for key, title, _ in t['sections'])
    schema = {'@context': 'https://schema.org', '@graph': [
        {'@type': 'WebPage', '@id': url + '#page', 'name': t['title'], 'description': t['description'], 'url': url, 'inLanguage': locale, 'dateModified': UPDATED,
         'isPartOf': {'@id': base + '/#website'}, 'about': {'@id': base + '/#app'}, 'breadcrumb': {'@id': url + '#breadcrumb'}},
        {'@type': 'BreadcrumbList', '@id': url + '#breadcrumb', 'itemListElement': [
            {'@type': 'ListItem', 'position': 1, 'name': t['home'], 'item': base + home},
            {'@type': 'ListItem', 'position': 2, 'name': t['title'], 'item': url}]}]}
    return f'''<!doctype html>
<html lang="{locale}"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{e(t['title'])} — no-sleep-pika</title><meta name="description" content="{e(t['description'])}">
<meta name="robots" content="index,follow,max-image-preview:large"><link rel="canonical" href="{url}">
<link rel="alternate" hreflang="en" href="{base}/guide/"><link rel="alternate" hreflang="ko" href="{base}/guide/ko/"><link rel="alternate" hreflang="x-default" href="{base}/guide/">
<meta property="og:type" content="article"><meta property="og:site_name" content="no-sleep-pika"><meta property="og:title" content="{e(t['title'])}"><meta property="og:description" content="{e(t['description'])}"><meta property="og:url" content="{url}"><meta property="og:image" content="{base}/assets/pika-working.png"><meta name="twitter:card" content="summary_large_image">
<link rel="icon" href="/assets/favicon.svg" type="image/svg+xml"><link rel="stylesheet" href="/install/install.css"><link rel="stylesheet" href="/guide/guide.css">
<script type="application/ld+json">{json.dumps(schema, ensure_ascii=False)}</script></head>
<body><a class="skip" href="#main">{e(t['title'])}</a><div class="shell"><header><a class="brand" href="{home}"><img src="/assets/favicon.svg" alt="" width="30" height="30">no-sleep-pika.</a><nav aria-label="{e(t['language'])}"><a href="/guide/" lang="en"{' aria-current="page"' if locale == 'en' else ''}>English</a><a href="/guide/ko/" lang="ko"{' aria-current="page"' if locale == 'ko' else ''}>한국어</a></nav></header>
<main id="main"><a class="back" href="{home}">← {e(t['home'])}</a><h1>{e(t['title'])}</h1><p class="intro">{e(t['intro'])}</p><p class="muted"><time datetime="{UPDATED}">{e(t['updated'])}</time></p>
<nav class="contents" aria-label="{e(t['title'])}">{contents}<a href="#mcp">{e(t['mcp'])}</a></nav>
<div class="guide-layout"><article>{sections}<section id="mcp"><h2>{e(t['mcp'])}</h2><p>{e(t['mcp_intro'])}</p><p>{e(t['mcp_cli'])}</p><pre><code>codex mcp add pika -- {COMMAND}</code></pre><p>{e(t['mcp_manual'])}</p><pre><code>[mcp_servers.pika]
command = "{COMMAND}"</code></pre><p>{e(t['mcp_check'])}</p><p>{e(t['mcp_tools'])}</p><pre><code>{COMMAND}</code></pre><p>{e(t['mcp_stop'])}</p></section></article>
<aside class="notice"><h2>{e(t['help'])}</h2><p>{e(t['help_body'])}</p><a href="{install}">{e(t['install'])} →</a></aside></div>
</main><footer><a href="{repo}/issues">{e(t['source'])} ↗</a><a href="https://support.apple.com/{'ko-kr' if locale == 'ko' else 'en-us'}/101588">{e(t['apple'])} ↗</a></footer></div></body></html>'''


def build(out, base, repo):
    for locale in COPY:
        directory = out / 'guide' / ('ko' if locale == 'ko' else '')
        directory.mkdir(parents=True, exist_ok=True)
        (directory / 'index.html').write_text(render(locale, base, repo), encoding='utf-8')
    return [base + '/guide/', base + '/guide/ko/']
