"""Small, bilingual installation guide, also readable when macOS blocks the app."""
import html
import json

COPY = {
'en': {
    'title': 'Install pika on Mac: PKG and helper setup', 'description': 'Install pika in Applications with its helper using one PKG. Follow macOS security prompts, quit older versions, and troubleshoot helper installation failures.',
    'back': 'Back', 'skip': 'Skip to instructions', 'language': 'Guide language',
    'intro': 'A home in Applications. Controls in your menu bar.',
    'languages': 'This guide is available in English and Korean. Other languages use English.',
    'steps': [
        ('Quit the previous pika', 'Turn Session OFF, then choose pika → Quit in the menu bar. Closing the window with × keeps the app running.'),
        ('Run the PKG installer', 'Open the downloaded pika PKG, continue through macOS Installer and approve installation as an administrator. The app and helper are installed together.'),
        ('Open pika', 'Open pika from Applications. The control window appears in front. Wait for helper connection, then turn Session ON and close the lid.')],
    'applications': 'Applications', 'open': 'Open', 'security': 'Privacy & Security', 'allow': 'Open Anyway',
    'warning': 'If macOS blocks the PKG or pika because the developer is unidentified or it cannot verify the app: open System Settings → Privacy & Security → Open Anyway, only if you trust this download. This build is not Developer ID signed or notarized.',
    'apple': 'Apple’s instructions for opening an app',
    'do_not': 'If macOS says the app will damage your computer or is damaged, stop and check the download; this is a different warning.',
    'helper_title': 'App opened, but Session will not start?',
    'helper_intro': 'Opening the app and installing its helper are separate steps. “Open Anyway” alone does not repair a helper connection.',
    'helper_steps': ['Download the latest full pika PKG from the homepage.', 'Turn Session OFF and quit pika from the menu bar before running the installer.', 'Complete installation and reopen pika. If it fails again, use Installer → Window → Installer Log to check the reason.'],
    'helper_note': 'The helper enables privileged power controls. Review the installer before approving. If macOS blocks that installer, follow the same app-specific Open Anyway flow only if you trust it.',
    'github': 'GitHub installation documentation', 'ready': 'When ready: Session ON → close your MacBook’s lid.',
},
'ko': {
    'title': 'Mac에 pika 설치하기: PKG와 보조 서비스', 'description': 'PKG 하나로 pika와 보조 서비스를 응용 프로그램에 설치하세요. 기존 앱 종료, macOS 보안 경고와 보조 서비스 설치 실패 해결 방법을 안내합니다.',
    'back': '홈으로', 'skip': '설치 안내로 이동', 'language': '안내 언어',
    'intro': '응용 프로그램에 설치하고, 메뉴 막대에서 사용하세요.',
    'languages': '이 안내는 한국어와 영어를 지원합니다. 그 외 언어는 영어로 표시됩니다.',
    'steps': [
        ('기존 pika 종료', 'Session을 OFF로 바꾼 뒤 메뉴 막대의 pika → 종료를 선택하세요. 창의 ×를 누르면 앱은 계속 실행 중입니다.'),
        ('PKG 설치', '다운로드한 pika PKG를 열고 macOS 설치 프로그램에서 계속 진행해 관리자 승인을 완료하세요. 앱과 보조 서비스가 함께 설치됩니다.'),
        ('pika 실행', '응용 프로그램에서 pika를 여세요. 제어창이 전면에 나타납니다. 보조 서비스 연결을 확인하고 Session ON → 덮개 닫기 순서로 사용하세요.')],
    'applications': 'Applications', 'open': '열기', 'security': '개인정보 보호 및 보안', 'allow': '그래도 열기',
    'warning': 'PKG나 pika 실행 시 개발자를 확인하거나 앱을 검증할 수 없다는 경고가 나오면, 출처를 신뢰할 때만 시스템 설정 → 개인정보 보호 및 보안 → 그래도 열기를 선택하세요. 현재 빌드는 Developer ID 서명·공증이 없습니다.',
    'apple': 'Apple 공식 앱 실행 안내',
    'do_not': '“컴퓨터를 손상시킵니다” 또는 “앱이 손상되었습니다”라는 경고는 다릅니다. 이 경우 진행하지 말고 다운로드를 확인하세요.',
    'helper_title': '앱은 열렸는데 Session이 시작되지 않나요?',
    'helper_intro': '앱 실행 허용과 보조 서비스 설치는 별개입니다. “그래도 열기”만으로 보조 서비스 연결 문제가 해결되는 것은 아닙니다.',
    'helper_steps': ['홈페이지에서 최신 pika 통합 PKG를 받으세요.', 'Session을 OFF로 바꾸고 메뉴 막대에서 pika를 종료한 뒤 PKG를 실행하세요.', '설치 완료 후 pika를 다시 여세요. 다시 실패하면 설치 프로그램 → 윈도우 → 설치 프로그램 로그에서 이유를 확인할 수 있습니다.'],
    'helper_note': '보조 서비스는 관리자 권한이 필요한 전원 제어를 담당합니다. 설치 내용을 확인한 뒤 승인하세요. 설치 파일도 macOS에 차단되면 출처를 신뢰할 때만 같은 “그래도 열기” 절차를 사용하세요.',
    'github': 'GitHub 설치 문서', 'ready': '준비되면: Session ON → 맥북 덮개 닫기.',
}}


def render(locale, base, repo):
    t = COPY[locale]
    e = html.escape
    url = base + ('/install/ko/' if locale == 'ko' else '/install/')
    home = '/ko/' if locale == 'ko' else '/'
    guide = '/guide/ko/' if locale == 'ko' else '/guide/'
    def visual(index):
        # Abstract diagrams, not screenshots or interactive system controls.
        if index == 0:
            return '<div class="diagram"><div class="mini-window"><strong>pika</strong><span>Session OFF</span><span>Quit · 종료</span></div></div>'
        if index == 1:
            return '<div class="diagram"><span class="app-icon">PKG</span><span class="arrow" aria-hidden="true">→</span><div class="mini-window"><strong>pika</strong><span>App + Helper</span></div></div>'
        return '<div class="diagram"><span class="app-icon">pika</span><span class="arrow" aria-hidden="true">→</span><div class="mini-window"><span class="window-dots">● ● ●</span><strong>pika</strong><span>Session <i></i></span><span>Monitor <i></i></span></div></div>'
    steps = ''.join(f'<li><span class="step-number">{i+1:02}</span>{visual(i)}<h2>{e(title)}</h2><p>{e(body)}</p></li>' for i, (title, body) in enumerate(t['steps']))
    helper = ''.join(f'<li>{e(step)}</li>' for step in t['helper_steps'])
    schema = {'@context': 'https://schema.org', '@type': 'WebPage', 'name': t['title'], 'description': t['description'], 'url': url, 'inLanguage': locale, 'dateModified': '2026-09-30', 'isPartOf': {'@id': base + '/#website'}, 'about': {'@id': base + '/#app'}}
    return f'''<!doctype html>
<html lang="{locale}"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{e(t['title'])} — no-sleep-pika</title><meta name="description" content="{e(t['description'])}">
<meta name="robots" content="index,follow,max-image-preview:large"><meta property="og:type" content="article"><meta property="og:site_name" content="no-sleep-pika"><meta property="og:title" content="{e(t['title'])}"><meta property="og:description" content="{e(t['description'])}"><meta property="og:url" content="{url}"><meta property="og:image" content="{base}/assets/pika-working.png"><meta name="twitter:card" content="summary_large_image">
<link rel="canonical" href="{url}"><link rel="alternate" hreflang="en" href="{base}/install/"><link rel="alternate" hreflang="ko" href="{base}/install/ko/"><link rel="alternate" hreflang="x-default" href="{base}/install/">
<link rel="icon" href="/assets/favicon.svg" type="image/svg+xml"><link rel="stylesheet" href="/install/install.css"><script src="/install/install.js" defer></script>
<script type="application/ld+json">{json.dumps(schema, ensure_ascii=False)}</script></head>
<body><a class="skip" href="#main">{e(t['skip'])}</a><div class="shell"><header><a class="brand" href="{home}"><img src="/assets/favicon.svg" alt="" width="30" height="30">no-sleep-pika.</a><nav aria-label="{e(t['language'])}"><a href="/install/" lang="en"{' aria-current="page"' if locale == 'en' else ''}>English</a><a href="/install/ko/" lang="ko"{' aria-current="page"' if locale == 'ko' else ''}>한국어</a></nav></header>
<main id="main"><a class="back" href="{home}">← {e(t['back'])}</a><h1>{e(t['title'])}</h1><p class="intro">{e(t['intro'])}</p><ol class="steps">{steps}</ol>
<aside class="notice"><p>{e(t['warning'])}</p><p>{e(t['do_not'])}</p><a href="https://support.apple.com/{'ko-kr' if locale == 'ko' else 'en-us'}/102445">{e(t['apple'])} ↗</a></aside>
<section class="helper" aria-labelledby="helper-title"><h2 id="helper-title">{e(t['helper_title'])}</h2><p>{e(t['helper_intro'])}</p><ol>{helper}</ol><p class="muted">{e(t['helper_note'])}</p><p class="ready">{e(t['ready'])}</p></section>
</main><footer><a href="{guide}">{'덮개·잠금·네트워크·MCP 사용 안내' if locale == 'ko' else 'Lid, lock, network & MCP guide'} →</a><a href="{repo}#readme">{e(t['github'])} ↗</a><p>{e(t['languages'])}</p></footer></div></body></html>'''


def build(out, base, repo):
    for locale in COPY:
        directory = out / 'install' / ('ko' if locale == 'ko' else '')
        directory.mkdir(parents=True, exist_ok=True)
        (directory / 'index.html').write_text(render(locale, base, repo), encoding='utf-8')
    return [base + '/install/', base + '/install/ko/']
