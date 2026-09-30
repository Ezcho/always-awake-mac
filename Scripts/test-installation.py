#!/usr/bin/env python3
"""Exercise real signed helper discovery without privileges or power mutations."""
from pathlib import Path
import subprocess, plistlib

app = Path(__file__).resolve().parent.parent / "dist/pika.app"
helper = app / "Contents/Library/HelperTools/AlwaysAwakeHelper"
for argv0 in [str(helper), "Contents/Library/HelperTools/AlwaysAwakeHelper", "AlwaysAwakeHelper"]:
    result = subprocess.run(
        [argv0, "--check-installation"], executable=str(helper), cwd="/",
        text=True, capture_output=True, timeout=15, check=True,
    )
    prefix = "Installation verified: "
    assert result.stdout.startswith(prefix), result.stdout
    assert Path(result.stdout.strip()[len(prefix):]).samefile(app), result.stdout
    print(f"PASS: signed app discovery with argv[0]={argv0!r}")

# Updates use Apple's Installer; do not ship a separately blocked executable.
assert not (app / "Contents/MacOS/pika-updater").exists()
print("PASS no standalone updater executable in bundle")

info = plistlib.loads((app/'Contents/Info.plist').read_bytes())
assert info['CFBundleExecutable'] == 'pika'
main = app/'Contents/MacOS'/info['CFBundleExecutable']
assert main.is_file() and not (app/'Contents/MacOS/AlwaysAwake').exists()
subprocess.run(['codesign','--verify','--strict',str(main)],check=True)
archs = subprocess.check_output(['lipo','-archs',str(main)],text=True)
assert 'arm64' in archs and 'x86_64' in archs
print('PASS renamed Universal pika executable and bundle entry point')
