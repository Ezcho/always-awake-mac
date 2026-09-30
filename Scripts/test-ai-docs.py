#!/usr/bin/env python3
"""Verify AI exports preserve code, cover publication inventory and remain current."""
from pathlib import Path
import re
import tempfile
import xml.etree.ElementTree as ET
from urllib.robotparser import RobotFileParser
from ai_docs import Markdown, build

ROOT = Path(__file__).resolve().parent.parent / 'docs'
BASE = 'https://no-sleep-pika.online'
ns = {'s': 'http://www.sitemaps.org/schemas/sitemap/0.9'}
index = (ROOT / 'llms.txt').read_text()
full = (ROOT / 'llms-full.txt').read_text()
urls = [node.text for node in ET.parse(ROOT / 'sitemap.xml').findall('s:url/s:loc', ns)]
for url in urls:
    html = ROOT / url.removeprefix(BASE).lstrip('/') / 'index.html'
    doc = Markdown(url)
    doc.feed(html.read_text())
    md = html.with_suffix('.md')
    assert md.read_text() == doc.text(), ('stale Markdown', md)
    assert BASE + '/' + md.relative_to(ROOT).as_posix() in index, ('missing index entry', md)
    assert doc.text() in full, ('missing full-text page', md)
    assert 'type="text/markdown"' in html.read_text(), ('missing discovery link', html)
    assert '<svg' not in md.read_text() and 'gtag(' not in md.read_text()
    assert md.read_text().count('```') % 2 == 0, ('broken code fence', md)

parser = RobotFileParser()
parser.parse((ROOT / 'robots.txt').read_text().splitlines())
for agent in ['OAI-SearchBot', 'ChatGPT-User', 'Claude-SearchBot', 'Claude-User', 'Googlebot', 'GPTBot', 'ClaudeBot']:
    for path in ['/llms.txt', '/llms-full.txt', '/guide/index.md', '/ko/']:
        assert parser.can_fetch(agent, BASE + path), (agent, path)

# Future articles are included from the sitemap, without a hand-maintained list.
with tempfile.TemporaryDirectory() as tmp:
    out = Path(tmp)
    (out / 'new').mkdir()
    (out / 'new/index.html').write_text('<html lang="en"><head><title>Future article</title></head><body><main><h1>New article</h1><pre><code>a = 1\n  b &lt; 2</code></pre><p><a href="/guide/">Guide</a></p><code>[server]\ncommand = &quot;pika&quot;</code><svg><text>ARTWORK</text></svg><button>Copy</button></main></body></html>')
    (out / 'sitemap.xml').write_text(f'<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"><url><loc>{BASE}/new/</loc></url></urlset>')
    build(out, BASE)
    result = (out / 'new/index.md').read_text()
    assert 'a = 1\n  b < 2' in result, 'code whitespace lost'
    assert '```\n[server]\ncommand = "pika"\n```' in result, 'multiline inline code lost'
    assert f'[Guide]({BASE}/guide/)' in result, 'relative link lost'
    assert 'ARTWORK' not in result and 'Copy' not in result
    assert BASE + '/new/index.md' in (out / 'llms.txt').read_text()
    before = {p.name: p.read_bytes() for p in out.rglob('*') if p.is_file()}
    build(out, BASE)
    assert before == {p.name: p.read_bytes() for p in out.rglob('*') if p.is_file()}, 'non-idempotent generation'
print(f'PASS {len(urls)} Markdown exports, full-text bundle, discovery, crawler access, code fidelity and future article coverage')
