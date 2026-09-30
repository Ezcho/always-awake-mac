#!/usr/bin/env python3
import copy
import hashlib
import importlib.util
from pathlib import Path
import tempfile
import unittest

spec = importlib.util.spec_from_file_location('feed', Path(__file__).with_name('publish-update-feed.py'))
feed = importlib.util.module_from_spec(spec)
spec.loader.exec_module(feed)

class FeedTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.package = self.root / 'pika-1.0.12.pkg'
        self.package.write_bytes(b'isolated package fixture')
        self.output = self.root / 'updates'
        self.release = {'tag_name': 'v1.0.12', 'draft': False, 'prerelease': False,
                        'published_at': '2026-10-01T00:00:00Z', 'assets': [{
            'name': self.package.name, 'browser_download_url': f'{feed.REPO}/releases/download/v1.0.12/{self.package.name}',
            'digest': 'sha256:' + hashlib.sha256(self.package.read_bytes()).hexdigest(),
            'size': self.package.stat().st_size}]}

    def test_published_matching_package(self):
        feed.publish(self.release, self.package, self.output)
        self.assertEqual((self.output / 'latest.json').read_bytes(), (self.output / 'v1.0.12.json').read_bytes())
        feed.publish(self.release, self.package, self.output)  # identical is idempotent

    def test_invalid_release(self):
        for edits in [{'draft': True}, {'prerelease': True}, {'published_at': None}, {'tag_name': 'v../latest'}]:
            with self.subTest(edits=edits), self.assertRaises(ValueError):
                feed.publish(self.release | edits, self.package, self.output)
        self.assertFalse(self.output.exists())

    def test_mismatching_asset(self):
        for field, value in [('digest', 'sha256:' + 'a' * 64), ('size', 1), ('browser_download_url', 'https://evil.invalid/a.pkg')]:
            release = copy.deepcopy(self.release)
            release['assets'][0][field] = value
            with self.subTest(field=field), self.assertRaises(ValueError):
                feed.publish(release, self.package, self.output)

    def test_immutable_version(self):
        feed.publish(self.release, self.package, self.output)
        self.package.write_bytes(b'different package')
        self.release['assets'][0].update(size=self.package.stat().st_size, digest='sha256:' + hashlib.sha256(self.package.read_bytes()).hexdigest())
        with self.assertRaises(ValueError):
            feed.publish(self.release, self.package, self.output)

    def test_no_downgrade(self):
        self.output.mkdir()
        (self.output / 'latest.json').write_text('{"tag_name":"v1.0.13"}')
        with self.assertRaises(ValueError):
            feed.publish(self.release, self.package, self.output)
        feed.publish(self.release, self.package, self.output, latest=False)
        self.assertIn('v1.0.13', (self.output / 'latest.json').read_text())

if __name__ == '__main__':
    unittest.main()
