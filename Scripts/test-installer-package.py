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
# Exercise the production installer parser with fake pmset output only.
sleep_function = 'sleep_enabled() {' + common.split('sleep_enabled() {',1)[1].split('\nrequire_sleep_enabled()',1)[0]
sleep_function = sleep_function.replace('/usr/bin/pmset -g', 'fake_pmset')
import shlex
cases = [
    ('System-wide power settings:\n SleepDisabled 0\n',0,0),
    ('System-wide power settings:\n SleepDisabled 1\n',0,1),
    ('System-wide power settings:\nCurrently in use:\n sleep 1\n',0,0),
    ('System-wide power settings:\n DestroyFVKeyOnStandby 1\n',0,0),
    ('',0,1), ('permission denied',1,1),
    ('Currently in use:\n sleep 1\n',0,1),
    ('System-wide power settings:\n SleepDisabled unknown\n',0,1),
    ('System-wide power settings:\n SleepDisabled 0\n SleepDisabled 1\n',0,1),
    ('System-wide power settings:\n SleepDisabled 0\n',1,1),
]
for output, exit_status, expected in cases:
    script = "set -euo pipefail\nfake_pmset() { printf '%s' " + shlex.quote(output) + f'; return {exit_status}; }}\n' + sleep_function + '\nsleep_enabled\n'
    result = subprocess.run(['/bin/bash','-c',script],capture_output=True,text=True)
    assert result.returncode == expected, (output,result.stderr)
print('PASS 10 installer power preflight cases without reading or changing host power settings')
# Simulate launchd and elapsed polling; never inspect, signal or unload host jobs.
stop_function = 'stop_installed_helper() {' + common.split('stop_installed_helper() {',1)[1].split('\nrequire_helper_running()',1)[0]
running_function = 'require_helper_running() {' + common.split('require_helper_running() {',1)[1]
def mock_commands(function):
    return function.replace('/bin/launchctl', 'fake_launchctl').replace('/bin/kill', 'fake_kill').replace('/bin/sleep', 'fake_sleep')
for exit_after, bootout_status, journal_present, expected in [(0,0,False,0),(30,0,False,0),(200,0,False,1),(0,1,False,1),(0,0,True,1)]:
    with tempfile.TemporaryDirectory() as tmp:
        journal = Path(tmp)/'journal'
        if journal_present: journal.write_text('recovery intent')
        script = f'''set -euo pipefail
LABEL=test
JOURNAL={shlex.quote(str(journal))}
loaded=1
probes=0
fail() {{ echo "$*" >&2; exit 1; }}
require_sleep_enabled() {{ return 0; }}
fake_sleep() {{ :; }}
fake_launchctl() {{
    if [[ "$1" == print ]]; then
        [[ "$loaded" == 1 ]] || return 1
        echo 'pid = 12345'
    else
        loaded=0
        return {bootout_status}
    fi
}}
fake_kill() {{ probes=$((probes + 1)); (( probes <= {exit_after} )); }}
''' + mock_commands(stop_function) + '\nstop_installed_helper\n'
        result = subprocess.run(['/bin/bash','-c',script],capture_output=True,text=True,timeout=5)
        assert result.returncode == expected, (exit_after,bootout_status,journal_present,result.stderr)
        assert journal.exists() == journal_present, 'Recovery record must never be removed'
print('PASS 5 helper shutdown cases, including a shutdown beyond the old five-second limit')
for scenario, expected in [('stable',0),('delayed',0),('crash',1),('flapping',1),('dead_pid',1)]:
    with tempfile.TemporaryDirectory() as tmp:
        counter = Path(tmp)/'polls'
        counter.write_text('0')
        script = f'''set -euo pipefail
LABEL=test
COUNTER={shlex.quote(str(counter))}
SCENARIO={shlex.quote(scenario)}
fail() {{ echo "$*" >&2; exit 1; }}
fake_sleep() {{ :; }}
fake_kill() {{ [[ "$SCENARIO" != dead_pid ]]; }}
fake_launchctl() {{
    local count
    count=$(cat "$COUNTER")
    count=$((count + 1))
    echo "$count" > "$COUNTER"
    case "$SCENARIO" in
        crash) echo 'state = waiting'; return 0 ;;
        delayed) if (( count < 20 )); then return 1; fi ;;
        flapping) echo "pid = $((12345 + count % 2))"; return 0 ;;
    esac
    echo 'pid = 12345'
}}
''' + mock_commands(running_function) + '\nrequire_helper_running\n'
        result = subprocess.run(['/bin/bash','-c',script],capture_output=True,text=True,timeout=10)
        assert result.returncode == expected, (scenario,result.stderr)
print('PASS 5 startup cases: running/delayed accepted; crash loop, changing PID and dead PID rejected')
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
    assert info['CFBundleVersion']==plistlib.loads((root/'Resources/Info.plist').read_bytes())['CFBundleVersion']
    payload = apps[0].parent.parent
    helper = payload/'Library/PrivilegedHelperTools/com.alwaysawake.mac.installed.helper'
    pin = payload/'Library/Application Support/pika/installed-client.requirement'
    assert helper.is_file() and pin.is_file()
    subprocess.run(['codesign','--verify','--deep','--strict','-R='+pin.read_text().strip(),str(apps[0])],check=True)
    assert helper.read_bytes()==(apps[0]/'Contents/Library/HelperTools/AlwaysAwakeHelper').read_bytes()
    for name in ['common.sh','preinstall','postinstall']:
        packaged = list(expanded.glob('**/Scripts/'+name))
        assert len(packaged)==1, (name,packaged)
        source = root/'Resources/Installer'/('' if name=='common.sh' else 'install')/name
        assert packaged[0].read_bytes()==source.read_bytes(), f'Stale packaged script: {name}'
print('PASS full PKG: must-close, install guidance, version, app/helper payload and exact client signature pin')
