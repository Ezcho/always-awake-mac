#!/usr/bin/env python3
"""Save a public GitHub release-download snapshot. Never count clicks as downloads."""
import json
import os
import re
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

API = 'https://api.github.com/repos/Ezcho/always-awake-mac'

def get_pages(endpoint):
    items = []
    for page in range(1, 101):
        headers = {'Accept': 'application/vnd.github+json', 'User-Agent': 'pika-download-counter'}
        if os.environ.get('GITHUB_TOKEN'):
            headers['Authorization'] = 'Bearer ' + os.environ['GITHUB_TOKEN']
        request = urllib.request.Request(f'{API}/{endpoint}?per_page=100&page={page}', headers=headers)
        with urllib.request.urlopen(request, timeout=20) as response:
            batch = json.load(response)
        if not isinstance(batch, list):
            raise ValueError('Unexpected GitHub response')
        items.extend(batch)
        if len(batch) < 100:
            return items
    raise ValueError('Incomplete pagination; previous snapshot preserved')

def main():
    assets = {}
    for release in get_pages('releases'):
        if release.get('draft'):
            continue
        for asset in get_pages(f"releases/{release['id']}/assets"):
            name = asset['name']
            if re.search(r'\.(dmg|zip|pkg)$', name, re.I) and not re.search(r'uninstall', name, re.I):
                count = asset['download_count']
                if not isinstance(count, int) or count < 0:
                    raise ValueError('Invalid download count')
                assets[asset['id']] = {'name': name, 'downloads': count}
    result = {'total': sum(a['downloads'] for a in assets.values()),
              'updatedAt': datetime.now(timezone.utc).isoformat(),
              'source': 'GitHub release assets', 'assets': list(assets.values())}
    destination = Path(__file__).resolve().parent.parent / 'docs' / 'downloads.json'
    destination.write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n')
    print(f"Saved {result['total']} downloads across {len(assets)} installer/archive assets")

if __name__ == '__main__':
    main()
