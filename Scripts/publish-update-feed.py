#!/usr/bin/env python3
"""Create static updater metadata only from a published release and verified local PKG.

After publishing immutable assets:
  gh api repos/Ezcho/always-awake-mac/releases/tags/vVERSION > .build/release.json
  python3 Scripts/publish-update-feed.py --release-json .build/release.json --package dist/pika-VERSION.pkg
Then commit docs/updates and deploy GitHub Pages. Never put a GitHub token in the feed.
"""
import argparse
import hashlib
import json
from pathlib import Path
import re

REPO = 'https://github.com/Ezcho/always-awake-mac'
VERSION = re.compile(r'(0|[1-9][0-9]{0,5})\.(0|[1-9][0-9]{0,5})\.(0|[1-9][0-9]{0,5})')


def publish(release, package, output, latest=True):
    tag = release.get('tag_name', '')
    version = tag.removeprefix('v')
    if not tag.startswith('v') or not VERSION.fullmatch(version):
        raise ValueError('Invalid release version')
    if release.get('draft') is not False or release.get('prerelease') is not False or not release.get('published_at'):
        raise ValueError('Release must already be publicly published')
    name = f'pika-{version}.pkg'
    assets = [a for a in release.get('assets', []) if a.get('name') == name]
    if len(assets) != 1 or package.name != name or package.is_symlink() or not package.is_file():
        raise ValueError('Expected exactly one matching release PKG')
    asset = assets[0]
    data = package.read_bytes()
    digest = 'sha256:' + hashlib.sha256(data).hexdigest()
    url = f'{REPO}/releases/download/{tag}/{name}'
    if asset.get('browser_download_url') != url or asset.get('digest') != digest or asset.get('size') != len(data) or not 0 < len(data) < 50_000_000:
        raise ValueError('Published asset URL, size and SHA256 must match the local PKG')
    manifest = {'tag_name': tag, 'draft': False, 'prerelease': False,
                'assets': [{'name': name, 'browser_download_url': url, 'digest': digest, 'size': len(data)}]}
    serialized = json.dumps(manifest, indent=2) + '\n'
    pinned = output / f'{tag}.json'
    if pinned.exists() and json.loads(pinned.read_text()) != manifest:
        raise ValueError('Cannot rewrite an immutable version feed')
    current = output / 'latest.json'
    if latest and current.exists():
        previous = json.loads(current.read_text())['tag_name'][1:]
        if tuple(map(int, previous.split('.'))) > tuple(map(int, version.split('.'))):
            raise ValueError('Cannot downgrade the latest feed')
    output.mkdir(parents=True, exist_ok=True)
    pinned.write_text(serialized)
    if latest:
        current.write_text(serialized)
    return manifest


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--release-json', required=True, type=Path)
    parser.add_argument('--package', required=True, type=Path)
    parser.add_argument('--output', type=Path, default=Path(__file__).resolve().parent.parent / 'docs/updates')
    parser.add_argument('--no-latest', action='store_true')
    args = parser.parse_args()
    result = publish(json.loads(args.release_json.read_text()), args.package, args.output, not args.no_latest)
    print(f"Verified static update feed: {result['tag_name']}")
