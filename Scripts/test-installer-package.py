#!/usr/bin/env python3
"""Inspect product packaging and process preflight without installing or killing apps."""
from pathlib import Path
import plistlib, subprocess, tempfile, xml.etree.ElementTree as ET
root = Path(__file__).resolve().parent.parent
common = (root/'Resources/Installer/common.sh').read_text()
function = common.split('require_app_closed() {',1)[1].split('\nstop_installed_helper()',1)[0]
function = ('require_app_closed() {'+function).replace('/usr/bin/pgrep -x AlwaysAwake', 'fake_pgrep')
for status, expected in [(0,1),(1,0),(2,1)]:
    script = f'set -euo pipefail\nfake_pgrep() {{ return {status}; }}\nfail() {{ echo "$*" >&2; exit 1; }}\n'+function+'\nrequire_app_closed\n'
    result = subprocess.run(['/bin/bash','-c',script],capture_output=True,text=True)
    assert result.returncode == expected, (status,result.stderr)
print('PASS process preflight: running app rejected, closed app allowed, inspection failure rejected')
version = plistlib.loads((root/'Resources/Info.plist').read_bytes())['CFBundleShortVersionString']
with tempfile.TemporaryDirectory(dir=root/'.build') as tmp:
    expanded = Path(tmp)/'product'
    subprocess.run(['pkgutil','--expand-full',str(root/f'dist/pika-{version}.pkg'),str(expanded)],check=True)
    distribution = ET.parse(expanded/'Distribution')
    assert distribution.find('.//must-close/app').attrib['id']=='com.alwaysawake.mac'
    assert distribution.find('welcome') is not None and distribution.find('conclusion') is not None
    assert distribution.find('domains').attrib['enable_anywhere']=='false'
    apps = list(expanded.glob('**/Payload/Applications/pika.app'))
    assert len(apps)==1
    info = plistlib.loads((apps[0]/'Contents/Info.plist').read_bytes())
    assert info['CFBundleShortVersionString']==version
    payload = apps[0].parent.parent
    helper = payload/'Library/PrivilegedHelperTools/com.alwaysawake.mac.installed.helper'
    pin = payload/'Library/Application Support/pika/installed-client.requirement'
    assert helper.is_file() and pin.is_file()
    subprocess.run(['codesign','--verify','--deep','--strict','-R='+pin.read_text().strip(),str(apps[0])],check=True)
    assert helper.read_bytes()==(apps[0]/'Contents/Library/HelperTools/AlwaysAwakeHelper').read_bytes()
print('PASS full PKG: must-close, install guidance, version, app/helper payload and exact client signature pin')
