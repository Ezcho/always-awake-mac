"""Small, bilingual installation guide, also readable when macOS blocks the app."""
import html
import json

COPY = {
'en': {
    'title': 'Install pika', 'description': 'Drag pika into Applications, open the app, and set up its helper service.',
    'back': 'Back', 'skip': 'Skip to instructions', 'language': 'Guide language',
    'intro': 'A home in Applications. Controls in your menu bar.',
    'languages': 'This guide is available in English and Korean. Other languages use English.',
    'steps': [
        ('Drag to Applications', 'Open the downloaded DMG. Drag pika onto Applications. If replacing a version, quit the old app first.'),
        ('Open pika', 'Open pika from Applications. Its controls appear in a window at launch; closing that window keeps pika in the menu bar.'),
        ('If macOS blocks opening', 'For an unidentified-developer or unverified-app warning, use System Settings → Privacy & Security → Open Anyway. Confirm Open only if you trust this download.')],
    'applications': 'Applications', 'open': 'Open', 'security': 'Privacy & Security', 'allow': 'Open Anyway',
    'warning': 'The current build is not Developer ID signed or notarized. macOS may stop it before pika can show its own guide. The steps here remain available in your browser.',
    'apple': 'Apple’s instructions for opening an app',
    'do_not': 'If macOS says the app will damage your computer or is damaged, stop and check the download; this is a different warning.',
    'helper_title': 'App opened, but Session will not start?',
    'helper_intro': 'Opening the app and installing its helper are separate steps. “Open Anyway” alone does not repair a helper connection.',
    'helper_steps': ['In pika’s setup guide, choose Install helper service.', 'Download the helper installer, then quit pika before opening it.', 'Complete the macOS Installer with your administrator approval, then reopen pika.'],
    'helper_note': 'The helper enables privileged power controls. Review the installer before approving. If macOS blocks that installer, follow the same app-specific Open Anyway flow only if you trust it.',
    'github': 'GitHub installation documentation', 'ready': 'When ready: Session ON → close your MacBook’s lid.',
},
'ko': {
    'title': 'pika 설치하기', 'description': 'pika를 응용 프로그램에 드래그하고 앱을 연 뒤 보조 서비스를 설정하세요.',
    'back': '홈으로', 'skip': '설치 안내로 이동', 'language': '안내 언어',
    'intro': '응용 프로그램에 설치하고, 메뉴 막대에서 사용하세요.',
    'languages': '이 안내는 한국어와 영어를 지원합니다. 그 외 언어는 영어로 표시됩니다.',
    'steps': [
        ('응용 프로그램으로 드래그', '다운로드한 DMG를 열고 pika를 Applications로 드래그하세요. 대치 설치라면 기존 앱을 먼저 종료하세요.'),
        ('pika 열기', '응용 프로그램 폴더에서 pika를 여세요. 실행하면 제어창이 나타나고, 창을 닫아도 메뉴 막대에서 계속 사용할 수 있습니다.'),
        ('macOS가 실행을 차단할 때만', '개발자를 확인할 수 없거나 앱을 검증할 수 없다는 경고라면 시스템 설정 → 개인정보 보호 및 보안 → 그래도 열기를 선택하세요. 출처를 신뢰할 때만 다시 열기를 승인하세요.')],
    'applications': 'Applications', 'open': '열기', 'security': '개인정보 보호 및 보안', 'allow': '그래도 열기',
    'warning': '현재 빌드는 Developer ID 서명·공증이 없어 pika의 안내창이 뜨기 전에 macOS가 실행을 막을 수 있습니다. 그때는 이 웹 안내를 이용하세요.',
    'apple': 'Apple 공식 앱 실행 안내',
    'do_not': '“컴퓨터를 손상시킵니다” 또는 “앱이 손상되었습니다”라는 경고는 다릅니다. 이 경우 진행하지 말고 다운로드를 확인하세요.',
    'helper_title': '앱은 열렸는데 Session이 시작되지 않나요?',
    'helper_intro': '앱 실행 허용과 보조 서비스 설치는 별개입니다. “그래도 열기”만으로 보조 서비스 연결 문제가 해결되는 것은 아닙니다.',
    'helper_steps': ['pika의 설치 안내에서 보조 서비스 설치를 선택하세요.', '보조 서비스 설치 파일을 다운로드하고, pika를 종료한 뒤 설치 파일을 여세요.', 'macOS 설치 프로그램에서 관리자 승인을 거쳐 완료한 다음 pika를 다시 실행하세요.'],
    'helper_note': '보조 서비스는 관리자 권한이 필요한 전원 제어를 담당합니다. 설치 내용을 확인한 뒤 승인하세요. 설치 파일도 macOS에 차단되면 출처를 신뢰할 때만 같은 “그래도 열기” 절차를 사용하세요.',
    'github': 'GitHub 설치 문서', 'ready': '준비되면: Session ON → 맥북 덮개 닫기.',
}}


def render(locale, base, repo):
    t = COPY[locale]
    e = html.escape
    url = base + ('/install/ko/' if locale == 'ko' else '/install/')
    home = '/ko/' if locale == 'ko' else '/'
    def visual(index):
        # Abstract diagrams, not screenshots or interactive system controls.
        if index == 0:
            return f'<div class="diagram"><span class="app-icon">pika</span><span class="arrow" aria-hidden="true">→</span><div class="folder"><svg viewBox="0 0 64 48" aria-hidden="true"><path d="M3 10h22l6 7h30v28H3z" fill="#b9cbaa"/><path d="M3 5h22l6 7h30v8H3z" fill="#99b47e"/></svg><small>{e(t["applications"])}</small></div></div>'
        if index == 1:
            return f'<div class="diagram"><span class="app-icon">pika</span><span class="arrow" aria-hidden="true">→</span><div class="mini-window"><span class="window-dots">● ● ●</span><strong>pika</strong><span>Session <i></i></span><span>Monitor <i></i></span></div></div>'
        return f'<div class="diagram"><div class="settings"><span>⚙ {e(t["security"])}</span><div><strong>pika</strong><span class="mock-button">{e(t["allow"])}</span></div></div></div>'
    steps = ''.join(f'<li><span class="step-number">{i+1:02}</span>{visual(i)}<h2>{e(title)}</h2><p>{e(body)}</p></li>' for i, (title, body) in enumerate(t['steps']))
    helper = ''.join(f'<li>{e(step)}</li>' for step in t['helper_steps'])
    schema = {'@context': 'https://schema.org', '@type': 'WebPage', 'name': t['title'], 'description': t['description'], 'url': url, 'inLanguage': locale}
    return f'''<!doctype html>
<html lang="{locale}"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{e(t['title'])} — no-sleep-pika</title><meta name="description" content="{e(t['description'])}">
<link rel="canonical" href="{url}"><link rel="alternate" hreflang="en" href="{base}/install/"><link rel="alternate" hreflang="ko" href="{base}/install/ko/"><link rel="alternate" hreflang="x-default" href="{base}/install/">
<link rel="icon" href="/assets/favicon.svg" type="image/svg+xml"><link rel="stylesheet" href="/install/install.css"><script src="/install/install.js" defer></script>
<script type="application/ld+json">{json.dumps(schema, ensure_ascii=False)}</script></head>
<body><a class="skip" href="#main">{e(t['skip'])}</a><div class="shell"><header><a class="brand" href="{home}"><img src="/assets/favicon.svg" alt="" width="30" height="30">no-sleep-pika.</a><nav aria-label="{e(t['language'])}"><a href="/install/" lang="en"{' aria-current="page"' if locale == 'en' else ''}>English</a><a href="/install/ko/" lang="ko"{' aria-current="page"' if locale == 'ko' else ''}>한국어</a></nav></header>
<main id="main"><a class="back" href="{home}">← {e(t['back'])}</a><h1>{e(t['title'])}</h1><p class="intro">{e(t['intro'])}</p><ol class="steps">{steps}</ol>
<aside class="notice"><p>{e(t['warning'])}</p><p>{e(t['do_not'])}</p><a href="https://support.apple.com/{'ko-kr' if locale == 'ko' else 'en-us'}/102445">{e(t['apple'])} ↗</a></aside>
<section class="helper" aria-labelledby="helper-title"><h2 id="helper-title">{e(t['helper_title'])}</h2><p>{e(t['helper_intro'])}</p><ol>{helper}</ol><p class="muted">{e(t['helper_note'])}</p><p class="ready">{e(t['ready'])}</p></section>
</main><footer><a href="{repo}#readme">{e(t['github'])} ↗</a><p>{e(t['languages'])}</p></footer></div></body></html>'''


def build(out, base, repo):
    for locale in COPY:
        directory = out / 'install' / ('ko' if locale == 'ko' else '')
        directory.mkdir(parents=True, exist_ok=True)
        (directory / 'index.html').write_text(render(locale, base, repo), encoding='utf-8')
    return [base + '/install/', base + '/install/ko/']
