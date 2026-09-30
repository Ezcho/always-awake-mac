"""Bilingual, server-rendered article for closed-lid MacBook workflows."""
import html
import json
from lid_article_locales import LANGUAGES, TRANSLATIONS

UPDATED = '2026-10-01'
PATHS = {locale: '/guide/' + ('' if locale == 'en' else locale + '/') + 'macbook-lid-closed/' for locale, _ in LANGUAGES}
COPY = {
    'ko': {
        'title': '맥북 덮어도 안꺼지게 하는법',
        'description': '맥북 덮개를 닫아도 작업을 유지하는 방법. 외장 모니터를 쓰는 클램쉘 모드와 화면 없이 pika로 다운로드·빌드·AI 에이전트를 실행하는 방법을 설명합니다.',
        'intro': '화면은 닫고, 하던 작업은 계속. 외장 모니터를 쓰는 경우와 백그라운드 작업만 필요한 경우를 나눠 알아봅니다.',
        'home': '홈', 'guide': '사용 가이드', 'language': '게시글 언어',
        'date': '2026년 10월 1일', 'label': 'MACBOOK GUIDE',
        'quick': '작업만 유지하려면', 'answer': 'pika 실행 → Session ON → Monitor OFF → 덮개 닫기',
        'detail': '덮개가 열려 있을 때 Session이나 Monitor를 바꿔도 화면을 즉시 끄지 않습니다.',
        'cta': 'pika 다운로드', 'install': '설치 방법', 'mcp': 'AI 에이전트 MCP 연결',
        'aside_title': '맥을 덮어도 작업을 유지하세요',
        'aside_body': 'pika는 Session과 Monitor 두 스위치로 제어하는 macOS 메뉴 막대 앱입니다. macOS 13 이상, Apple Silicon·Intel용입니다.',
        'disclosure': 'no-sleep-pika에서 작성한 자사 앱 사용 안내입니다.',
        'body': '''
<section id="sleep"><h2>덮으면 꺼지는 걸까요, 잠드는 걸까요?</h2>
<p>일반적으로 맥북 덮개를 닫으면 전원이 완전히 꺼지는 대신 잠자기 상태로 들어갑니다. 다시 열었을 때 앱이 그대로 보여도 그동안 빌드나 다운로드, AI 에이전트 작업이 계속 진행됐다는 뜻은 아닙니다. <a href="https://support.apple.com/ko-kr/guide/mac-help/mh10330/mac">Apple의 잠자기 안내</a>도 덮개 닫기를 잠자기 방법으로 설명합니다.</p>
<p>따라서 “맥북 덮어도 안 꺼지게” 하려면, 화면이 꺼지는 것과 시스템이 잠드는 것을 구분해야 합니다. 화면을 켜 둘 필요 없이 작업만 유지할 수도 있습니다.</p></section>
<section id="choose"><h2>외장 모니터를 쓰나요?</h2>
<div class="choices"><div><h3>외장 모니터로 계속 작업</h3><p>외장 화면·키보드·마우스를 연결해 덮고 쓰는 클램쉘 구성을 먼저 확인하세요. 이 용도라면 별도 절전 방지 앱이 필요하지 않을 수 있습니다.</p></div><div><h3>화면 없이 작업만 계속</h3><p>다운로드, 코드 빌드, AI 에이전트를 돌려 두려면 아래 pika 사용 순서를 따라가세요. 먼저 짧은 작업으로 자신의 Mac에서 동작을 확인하면 됩니다.</p></div></div>
<p>클램쉘 사용 전에는 덮개를 연 상태에서 외장 화면과 입력 장치가 정상 작동하는지 확인하세요. Apple Silicon Mac에서 액세서리 연결 승인을 요청하면 먼저 승인해야 합니다. <a href="https://support.apple.com/ko-kr/102282">Apple의 덮개를 닫은 상태에서 액세서리 사용 안내</a>에서 자세히 볼 수 있습니다. 전원과 지원 디스플레이 구성은 해당 Mac 모델의 안내를 함께 확인하세요.</p></section>
<section id="pika"><h2>외장 모니터 없이 pika로 작업 유지하기</h2>
<ol class="article-steps"><li><strong>pika를 설치하고 실행합니다.</strong> 홈페이지의 통합 PKG로 설치한 뒤 응용 프로그램 폴더의 pika를 여세요. 보조 서비스가 연결되어 있어야 합니다. 설치가 막히면 <a href="/install/ko/">설치 도움말</a>을 확인하세요.</li>
<li><strong>하던 작업을 시작하고 Session을 ON으로 바꿉니다.</strong> 덮개가 열린 상태에서는 화면을 즉시 끄거나 잠그지 않습니다.</li>
<li><strong>화면이 필요 없다면 Monitor를 OFF로 둡니다.</strong> Monitor는 Session이 켜져 있을 때 선택할 수 있고, 화면 동작은 덮개를 닫은 뒤 적용됩니다.</li>
<li><strong>맥북 덮개를 닫습니다.</strong> Session ON 상태에서 덮개를 닫으면 닫힌 덮개에 맞는 동작을 적용합니다. 통풍되는 책상 위에서 사용하세요.</li>
<li><strong>작업이 끝나면 Session을 OFF로 바꿉니다.</strong> pika가 관리하던 잠자기 설정을 복구합니다. Monitor 표시도 OFF가 되지만 화면을 즉시 끄지는 않습니다.</li></ol>
<p>제어창의 × 버튼은 창만 닫습니다. pika를 계속 사용하려면 메뉴 막대에서 실행 중인 상태로 두세요. 아이콘이 다른 항목에 가렸다면 응용 프로그램에서 pika를 다시 열어 제어창을 볼 수 있습니다.</p></section>
<section id="check"><h2>진짜 계속 실행되는지 확인하는 방법</h2>
<p>처음에는 완료까지 시간이 걸리며 진행 상황을 확인할 수 있는 작업으로 시험하세요. 예를 들어 작업 로그에 시간이 기록되는 빌드나 AI 에이전트 작업이 좋습니다.</p>
<ol><li>덮기 직전의 진행률이나 마지막 로그 시간을 확인합니다.</li><li>Session ON 상태에서 덮개를 닫고 잠시 기다립니다.</li><li>다시 열어 덮여 있던 시간에도 작업 로그나 진행률이 변했는지 확인합니다.</li></ol>
<p>잠금 화면이 나타났다는 이유만으로 실패한 것은 아닙니다. <strong>화면 잠금과 시스템 잠자기는 다릅니다.</strong> 판단 기준은 실제 작업의 진행 기록입니다. 다만 개별 앱이 입력이나 로그인을 기다리고 있으면 pika가 대신 진행해 주지는 않습니다.</p></section>
<section id="limits"><h2>배터리·발열·네트워크도 확인하세요</h2>
<p>pika는 배터리와 macOS의 열 상태를 확인해 보호 기준에 도달하면 세션을 중단할 수 있습니다. 외장 화면 없이 덮개를 닫은 상태에서는 더 보수적인 기준을 사용합니다. 이 기능이 밀폐된 가방 안에서의 사용을 안전하게 만들어 주는 것은 아닙니다.</p>
<p>잠자기를 막는 기능은 Wi-Fi나 VPN, 원격 API 연결을 보장하지 않습니다. 연결이 끊기거나 서비스 사용량 제한에 걸리면 AI 작업은 멈출 수 있습니다. 긴 작업에는 해당 도구의 재시도와 중간 저장 기능도 활용하세요.</p>
<p>현재 배포 파일은 Developer ID 서명·공증이 없어 macOS가 설치를 차단할 수 있습니다. 이 경우 <a href="/install/ko/">보안 경고와 설치 안내</a>를 확인하세요. macOS 버전이나 장비별 동작은 실제 사용 환경에서 확인해야 합니다.</p></section>
<section id="more"><h2>자주 묻는 질문</h2>
<h3>Session만 켜고 Monitor는 꺼도 되나요?</h3><p>네. 화면 없이 작업을 유지하려는 경우의 설정입니다. Session은 작업 유지, Monitor는 덮개를 닫은 뒤의 화면 동작을 담당합니다.</p>
<h3>덮개를 열면 화면이 바로 꺼지나요?</h3><p>pika는 덮개를 다시 열면 예약된 화면 끄기를 취소합니다. macOS 자체의 잠금·화면 설정은 별도로 적용됩니다.</p>
<h3>AI 에이전트가 Session을 제어할 수 있나요?</h3><p>같은 Mac에서 로컬 MCP 클라이언트를 연결하면 상태 확인과 Session·Monitor 제어가 가능합니다. <a href="/guide/ko/#mcp">MCP 연결 절차와 명령어</a>를 참고하세요.</p>
<p>연결 끊김이나 메뉴 막대 문제는 <a href="/guide/ko/">pika 전체 사용 가이드</a>에서 이어서 확인할 수 있습니다.</p></section>''',
        'sections': [('sleep', '잠자기와 종료'), ('choose', '사용 방식 선택'), ('pika', 'pika 사용 순서'), ('check', '동작 확인'), ('limits', '사용 조건'), ('more', '자주 묻는 질문')],
    },
    'en': {
        'title': 'How to keep a MacBook running with the lid closed',
        'description': 'Keep work running when you close your MacBook: choose an external-display setup or use pika for background downloads, builds and AI agents without a monitor.',
        'intro': 'Close the screen and keep your work going. Choose the approach that fits an external-display desk or a background task without a monitor.',
        'home': 'Home', 'guide': 'User guide', 'language': 'Article language',
        'date': 'October 1, 2026', 'label': 'MACBOOK GUIDE',
        'quick': 'For background work', 'answer': 'Open pika → Session ON → Monitor OFF → close the lid',
        'detail': 'Changing Session or Monitor with the lid open does not immediately blank your screen.',
        'cta': 'Download pika', 'install': 'Installation help', 'mcp': 'Connect an AI agent with MCP',
        'aside_title': 'Close your Mac. Keep work running.',
        'aside_body': 'pika is a macOS menu bar app with two switches: Session and Monitor. For macOS 13 or later on Apple Silicon and Intel.',
        'disclosure': 'Written by no-sleep-pika about our own app.',
        'body': '''
<section id="sleep"><h2>Closing the lid: sleep or shutdown?</h2>
<p>Closing a MacBook’s lid normally puts it to sleep rather than shutting it down. Finding your apps still open afterward does not mean a build, download or AI agent kept working throughout. <a href="https://support.apple.com/ko-kr/guide/mac-help/mh10330/mac">Apple’s sleep guide</a> lists closing a laptop display as a way to put the Mac to sleep.</p>
<p>The key distinction is between turning off a display and putting the system to sleep. A background task may need the Mac awake without needing a lit screen.</p></section>
<section id="choose"><h2>Are you using an external monitor?</h2>
<div class="choices"><div><h3>Keep working on another screen</h3><p>Check the Mac’s supported closed-display, or clamshell, setup with an external monitor, keyboard and mouse first. You may not need a separate sleep-prevention app for that workflow.</p></div><div><h3>Keep only a background task running</h3><p>For a download, code build or AI agent without an external screen, follow the pika steps below. Start with a short test on your own Mac.</p></div></div>
<p>Before closing the lid, check that the external display and input devices work. On an Apple Silicon Mac, approve an accessory connection if requested. <a href="https://support.apple.com/ko-kr/102282">Apple’s accessory guide</a> explains this for closed-lid use. Check your Mac model’s instructions for its power and supported display configuration.</p></section>
<section id="pika"><h2>Use pika without an external monitor</h2>
<ol class="article-steps"><li><strong>Install and open pika.</strong> Use the unified PKG from the homepage, then open pika in Applications. The helper must be connected. See <a href="/install/">installation help</a> if setup is blocked.</li>
<li><strong>Start your task and turn Session ON.</strong> This does not immediately blank or lock the screen while the lid is open.</li>
<li><strong>Leave Monitor OFF if you do not need a display.</strong> Monitor is available while Session is ON. Its display policy applies after you close the lid.</li>
<li><strong>Close the MacBook’s lid.</strong> With Session ON, pika applies its closed-lid behavior. Use a ventilated desk.</li>
<li><strong>Turn Session OFF when finished.</strong> pika restores the sleep setting it managed. Monitor also shows OFF, without immediately turning the screen off.</li></ol>
<p>The window’s × button only closes the controls. Leave pika running in the menu bar. If other status items hide its icon, open pika from Applications to bring the controls back.</p></section>
<section id="check"><h2>Check that your work actually continues</h2>
<p>First try a task whose progress you can inspect, such as a build or AI agent job with timestamped logs.</p>
<ol><li>Note the progress or last log timestamp before closing the lid.</li><li>Close the lid with Session ON and wait briefly.</li><li>Reopen it and check for progress recorded during the closed-lid interval.</li></ol>
<p>A lock screen alone does not mean the test failed. <strong>Screen lock and system sleep are different.</strong> Use your task’s progress as evidence. If an app is waiting for input or sign-in, pika cannot complete that interaction for you.</p></section>
<section id="limits"><h2>Battery, heat and network conditions still matter</h2>
<p>pika monitors battery level and macOS thermal state and may end a session when protection thresholds are reached. It uses more conservative limits with the lid closed and no external display. This does not make running a Mac inside a closed bag safe.</p>
<p>Preventing sleep does not guarantee Wi-Fi, VPN or remote API availability. A connection failure or service limit may stop an AI task. Use your tool’s supported retry and checkpoint features for long jobs.</p>
<p>The current download is not Developer ID signed or notarized, so macOS may block installation. Read the <a href="/install/">security warning and installation guide</a> if needed. Verify behavior on your actual macOS version and hardware.</p></section>
<section id="more"><h2>Common questions</h2>
<h3>Can I leave Session ON and Monitor OFF?</h3><p>Yes. That is the setup for work without a lit display. Session manages keeping work running; Monitor controls display behavior after the lid closes.</p>
<h3>Will reopening the lid turn the screen off?</h3><p>pika cancels its pending display-off work when the lid reopens. macOS’s own lock and display settings still apply.</p>
<h3>Can an AI agent control the session?</h3><p>A local MCP client on the same Mac can query status and control Session and Monitor. See the <a href="/guide/#mcp">MCP setup steps and commands</a>.</p>
<p>For connection issues and missing menu bar icons, continue to the <a href="/guide/">full pika user guide</a>.</p></section>''',
        'sections': [('sleep', 'Sleep and shutdown'), ('choose', 'Choose a setup'), ('pika', 'Use pika'), ('check', 'Verify progress'), ('limits', 'Conditions'), ('more', 'Questions')],
    },
}


# Every locale gets original HTML, a self-canonical URL and reciprocal alternates.
for locale, translation in TRANSLATIONS.items():
    e = html.escape
    ui = translation['ui']
    keys = ['sleep', 'choose', 'pika', 'check', 'limits']
    sections = list(zip(keys, translation['headings']))
    paragraphs = dict(translation)
    steps = '<ol class="article-steps">' + ''.join(f'<li>{e(step)}</li>' for step in translation['steps']) + '</ol>'
    body = ''
    for key, heading in sections:
        content = steps if key == 'pika' else '<p>' + e(paragraphs[key]) + '</p>'
        if key in ('sleep', 'choose'):
            source = 'https://support.apple.com/ko-kr/guide/mac-help/mh10330/mac' if key == 'sleep' else 'https://support.apple.com/ko-kr/102282'
            content += f'<p><a href="{source}">{e(translation["apple"])}</a></p>'
        body += f'<section id="{key}"><h2>{e(heading)}</h2>{content}</section>'
    body += f'<p><a href="/guide/" lang="en">{e(translation["more"])} · English →</a></p>'
    COPY[locale] = dict(translation, home=ui[0], guide=ui[1], language=ui[2], quick=ui[3], cta=ui[4], install=ui[5], mcp=ui[6], disclosure=ui[7], date=UPDATED, label='no-sleep-pika', aside_title=translation['title'], aside_body=translation['aside'], body=body, sections=sections)


def render(locale, base, repo):
    t, e = COPY[locale], html.escape
    body = t['body']
    if locale != 'ko':
        body = body.replace('https://support.apple.com/ko-kr/guide/mac-help/mh10330/mac', 'https://support.apple.com/en-gb/guide/mac-help/mh10330/mac').replace('https://support.apple.com/ko-kr/102282', 'https://support.apple.com/en-us/102282')
    url = base + PATHS[locale]
    home = '/' if locale == 'en' else '/' + locale + '/'
    guide = '/guide/ko/' if locale == 'ko' else '/guide/'
    install = '/install/ko/' if locale == 'ko' else '/install/'
    schema = {'@context': 'https://schema.org', '@graph': [
        {'@type': 'Article', '@id': url + '#article', 'headline': t['title'], 'description': t['description'],
         'mainEntityOfPage': url, 'url': url, 'inLanguage': locale,
         'datePublished': UPDATED, 'dateModified': UPDATED, 'image': base + '/assets/pika-working.png',
         'author': {'@type': 'Organization', 'name': 'no-sleep-pika', 'url': base + '/'},
         'publisher': {'@type': 'Organization', 'name': 'no-sleep-pika', 'url': base + '/'}},
        {'@type': 'BreadcrumbList', '@id': url + '#breadcrumb', 'itemListElement': [
            {'@type': 'ListItem', 'position': 1, 'name': t['home'], 'item': base + home},
            {'@type': 'ListItem', 'position': 2, 'name': t['guide'], 'item': base + guide},
            {'@type': 'ListItem', 'position': 3, 'name': t['title'], 'item': url}]}]}
    alternates = ''.join(f'<link rel="alternate" hreflang="{lang}" href="{base}{path}">' for lang, path in PATHS.items())
    language_names = dict(LANGUAGES)
    languages = ''.join(f'<a href="{path}" lang="{lang}"' + (' aria-current="page"' if locale == lang else '') + f'>{language_names[lang]}</a>' for lang, path in PATHS.items())
    contents = ''.join(f'<a href="#{key}">{e(title)}</a>' for key, title in t['sections'])
    return f'''<!doctype html>
<html lang="{locale}" dir="{'rtl' if locale == 'ar' else 'ltr'}"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{e(t['title'])} | no-sleep-pika</title><meta name="description" content="{e(t['description'])}">
<meta name="robots" content="index,follow,max-image-preview:large"><link rel="canonical" href="{url}">{alternates}<link rel="alternate" hreflang="x-default" href="{base}{PATHS['en']}">
<meta property="og:type" content="article"><meta property="og:site_name" content="no-sleep-pika"><meta property="og:title" content="{e(t['title'])}"><meta property="og:description" content="{e(t['description'])}"><meta property="og:url" content="{url}"><meta property="og:image" content="{base}/assets/pika-working.png"><meta property="article:published_time" content="{UPDATED}"><meta property="article:modified_time" content="{UPDATED}">
<meta name="twitter:card" content="summary_large_image"><meta name="twitter:title" content="{e(t['title'])}"><meta name="twitter:description" content="{e(t['description'])}"><meta name="twitter:image" content="{base}/assets/pika-working.png">
<link rel="icon" href="/assets/favicon.svg" type="image/svg+xml"><link rel="stylesheet" href="/install/install.css"><link rel="stylesheet" href="/guide/guide.css"><link rel="stylesheet" href="/guide/article.css">
<script type="application/ld+json">{json.dumps(schema, ensure_ascii=False)}</script><script src="/visitors.js" defer></script></head>
<body><a class="skip" href="#main">{e(t['title'])}</a><div class="shell"><header><a class="brand" href="{home}"><img src="/assets/favicon.svg" alt="" width="30" height="30">no-sleep-pika.</a><nav class="article-languages" aria-label="{e(t['language'])}"><details><summary>{language_names[locale]}</summary><div>{languages}</div></details></nav></header>
<main id="main"><a class="back" href="{guide}">← {e(t['guide'])}</a><p class="eyebrow">{t['label']}</p><h1>{e(t['title'])}</h1><p class="intro">{e(t['intro'])}</p><p class="muted">no-sleep-pika · <time datetime="{UPDATED}">{e(t['date'])}</time></p>
<div class="quick-answer"><span>{e(t['quick'])}</span><strong>{e(t['answer'])}</strong><p>{e(t['detail'])}</p></div>
<nav class="contents" aria-label="{e(t['guide'])}">{contents}</nav><div class="guide-layout"><article>{body}</article>
<aside class="notice"><img class="article-pika" src="/assets/pika-working.png" alt="" width="180" height="180"><h2>{e(t['aside_title'])}</h2><p>{e(t['aside_body'])}</p><a class="article-cta" href="{home}">{e(t['cta'])} →</a><a href="{install}">{e(t['install'])}</a><a href="{guide}#mcp">{e(t['mcp'])}</a></aside></div>
</main><footer><span>{e(t['disclosure'])}</span><a href="{repo}">GitHub ↗</a></footer></div></body></html>'''


def build(out, base, repo):
    for locale, path in PATHS.items():
        directory = out / path.strip('/')
        directory.mkdir(parents=True, exist_ok=True)
        (directory / 'index.html').write_text(render(locale, base, repo), encoding='utf-8')
    return [base + path for path in PATHS.values()]
