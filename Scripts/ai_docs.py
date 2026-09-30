"""Generate text documentation from the same public HTML shipped to readers."""
from html import escape
from html.parser import HTMLParser
from urllib.parse import urljoin
import re
import xml.etree.ElementTree as ET


class Markdown(HTMLParser):
    """Small converter for our generated pages; never includes scripts or artwork."""
    VOID = {'area', 'base', 'br', 'col', 'embed', 'hr', 'img', 'input', 'link', 'meta', 'param', 'source', 'track', 'wbr'}
    SKIP = {'script', 'style', 'svg', 'button', 'nav', 'form', 'noscript'}

    def __init__(self, url):
        super().__init__(convert_charrefs=True)
        self.url, self.parts, self.stack = url, [], []
        self.title, self.language = '', ''
        self.pre = 0
        self.code_start = None

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == 'html':
            self.language = attrs.get('lang', '')
        parent_active = self.stack[-1][1] if self.stack else False
        parent_skip = self.stack[-1][2] if self.stack else False
        skip = parent_skip or tag in self.SKIP or 'visitor-counter' in attrs.get('class', '')
        active = (parent_active or tag == 'main') and not skip
        href = urljoin(self.url, attrs.get('href', '')) if tag == 'a' else ''
        if tag not in self.VOID:
            self.stack.append((tag, active, skip, href))
        if not active:
            return
        if re.fullmatch(r'h[1-6]', tag):
            self.parts.append('\n\n' + '#' * int(tag[1]) + ' ')
        elif tag in {'p', 'section', 'article', 'div', 'details'}:
            self.parts.append('\n\n')
        elif tag == 'li':
            self.parts.append('\n- ')
        elif tag == 'br':
            self.parts.append('\n')
        elif tag == 'pre':
            self.parts.append('\n\n```\n')
            self.pre += 1
        elif tag == 'code' and not self.pre:
            self.code_start = len(self.parts)
            self.parts.append('`')
        elif tag in {'strong', 'b'}:
            self.parts.append('**')
        elif tag == 'a':
            self.parts.append('[')
        elif tag == 'tr':
            self.parts.append('\n')
        elif tag in {'td', 'th'}:
            self.parts.append(' | ')

    def handle_endtag(self, tag):
        if not self.stack or tag in self.VOID:
            return
        # HTML output is controlled; pop to the matching tag for optional endings.
        match = next((i for i in range(len(self.stack)-1, -1, -1) if self.stack[i][0] == tag), None)
        if match is None:
            return
        _, active, _, href = self.stack[match]
        del self.stack[match:]
        if not active:
            return
        if tag == 'pre':
            self.pre -= 1
            self.parts.append('\n```\n\n')
        elif tag == 'code' and not self.pre:
            content = ''.join(self.parts[self.code_start + 1:])
            if '\n' in content:
                self.parts[self.code_start:] = ['\n\n```\n', content, '\n```\n\n']
            else:
                self.parts.append('`')
            self.code_start = None
        elif tag in {'strong', 'b'}:
            self.parts.append('**')
        elif tag == 'a':
            self.parts.append(f']({href})')
        elif tag in {'p', 'section', 'article', 'div', 'li'} or re.fullmatch(r'h[1-6]', tag):
            self.parts.append('\n\n')

    def handle_data(self, data):
        if self.stack and self.stack[-1][0] == 'title':
            self.title += data
        if self.stack and self.stack[-1][1]:
            self.parts.append(data if self.pre or any(t[0] == 'code' for t in self.stack) else re.sub(r'\s+', ' ', data))

    def text(self):
        chunks = ''.join(self.parts).split('```')
        for i in range(0, len(chunks), 2):
            chunks[i] = re.sub(r'\n[ \t]+', '\n', chunks[i])
            chunks[i] = re.sub(r'\n{3,}', '\n\n', chunks[i])
        body = '```'.join(chunks).strip()
        return f'Source: {self.url}\nLanguage: {self.language}\n\n{body}\n'


def build(out, base):
    # Sitemap is the inventory: future published articles join automatically.
    ns = {'s': 'http://www.sitemaps.org/schemas/sitemap/0.9'}
    pages = ET.parse(out / 'sitemap.xml').findall('s:url', ns)
    records = []
    for item in pages:
        url = item.find('s:loc', ns).text
        path = out / url.removeprefix(base).lstrip('/') / 'index.html'
        source = path.read_text(encoding='utf-8')
        doc = Markdown(url)
        doc.feed(source)
        md = path.with_suffix('.md')
        md.write_text(doc.text(), encoding='utf-8')
        md_url = base + '/' + md.relative_to(out).as_posix()
        links = (f'<link rel="alternate" type="text/markdown" href="{escape(md_url, quote=True)}" title="Markdown">'
                 f'<link rel="help" type="text/plain" href="{base}/llms.txt" title="Documentation index">')
        # Idempotent even when invoked independently after site generation.
        source = re.sub(r'<link rel="alternate" type="text/markdown"[^>]*>', '', source)
        source = re.sub(r'<link rel="help" type="text/plain"[^>]*>', '', source)
        path.write_text(source.replace('</head>', links + '</head>'), encoding='utf-8')
        records.append((doc, md_url))
    header = '''# no-sleep-pika (pika)

> Native macOS menu-bar utility for keeping MacBook work running with the lid closed, with Session / Monitor controls and local MCP tools. macOS 13+, Apple Silicon and Intel.

Session ON prepares sleep prevention before lid closure. In closed-lid mode, display policy applies after the lid closes. A working administrator helper is required. Battery / thermal protection may end a session. pika does not guarantee network connectivity or resume failed AI jobs.

The bundled pika-mcp is a local STDIO server, not a public HTTP service. It exposes pika_status, pika_set_session and pika_set_monitor. It controls pika, not AI conversations. The website is not an MCP endpoint. pika is independent of OpenAI and Anthropic.

Markdown pages below are generated from the same HTML as the public website. Their Source field points to the human-readable canonical page. Publication makes content available for retrieval; it does not guarantee indexing, training, citation, or recommendation by any AI provider.
'''
    preferred = [r for r in records if r[0].language in ('en', 'ko') and '/guide/macbook-lid-closed/' not in r[0].url and '/guide/ko/macbook-lid-closed/' not in r[0].url]
    index = header + '\n## Core documentation\n\n'
    index += ''.join(f'- [{d.title} ({d.language})]({u})\n' for d, u in preferred)
    index += '\n## All localized pages and articles\n\n'
    index += ''.join(f'- [{d.title} ({d.language})]({u})\n' for d, u in records)
    index += f'\n## Optional\n\n- [Complete text collection]({base}/llms-full.txt): All published languages; use individual pages for smaller context.\n- [Source code and MCP reference](https://github.com/Ezcho/always-awake-mac#readme)\n- [Published releases](https://github.com/Ezcho/always-awake-mac/releases)\n'
    (out / 'llms.txt').write_text(index, encoding='utf-8')
    (out / 'llms-full.txt').write_text(header + '\n\n' + '\n\n---\n\n'.join(d.text() for d, _ in records), encoding='utf-8')
    return len(records)
