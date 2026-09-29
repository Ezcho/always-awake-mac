#!/usr/bin/env python3
"""Exercise real signed helper discovery without privileges or power mutations."""
from pathlib import Path
import subprocess

app = Path(__file__).resolve().parent.parent / "dist/Always Awake.app"
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
