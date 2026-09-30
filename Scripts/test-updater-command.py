"""Exercise private staging/quoting/checksum/failure with an inert fake installer. No sudo."""
from pathlib import Path
import os, subprocess
root = Path('.build/update-tests').resolve()
script = (root / 'install.sh').read_text()
installer = root / 'fake-installer'
marker = root / 'called'
installer.write_text('#!/bin/sh\nprintf called > "$PIKA_TEST_MARKER"\necho simulated-installer\nexit "${PIKA_TEST_EXIT:-0}"\n')
installer.chmod(0o700)
quote = lambda s: "'" + str(s).replace("'", "'\\''") + "'"
script = script.replace('/usr/sbin/installer', quote(installer))
env = dict(os.environ, PIKA_TEST_MARKER=str(marker))
marker.unlink(missing_ok=True)
result = subprocess.run(['/bin/bash', '-c', script], env=env, capture_output=True, text=True, timeout=15, cwd=root)
assert result.returncode == 0 and result.stdout.strip() == 'PIKA_UPDATE_OK', result
assert marker.exists() and not (root / 'INJECTED').exists()
print('PASS staged package, literal shell metacharacters, fake install success')
marker.unlink()
result = subprocess.run(['/bin/bash', '-c', script], env=dict(env, PIKA_TEST_EXIT='1'), capture_output=True, text=True, timeout=15, cwd=root)
assert result.returncode != 0 and 'simulated-installer' in result.stderr
print('PASS installer failure propagates diagnostic output')
marker.unlink()
pkg = next(root.glob('pika*.pkg'))
pkg.write_text('corrupt package')
result = subprocess.run(['/bin/bash', '-c', script], env=env, capture_output=True, text=True, timeout=15, cwd=root)
assert result.returncode != 0 and not marker.exists() and 'checksum mismatch' in result.stderr
print('PASS corrupted snapshot never reaches installer')
