#!/bin/bash
set -euo pipefail
cd "$(dirname "$0")/.."
mkdir -p .build/module-cache
xcrun swiftc -swift-version 5 -module-cache-path .build/module-cache Sources/Shared/Protocol.swift Sources/Shared/UpdateRelease.swift Sources/App/UpdateDownload.swift Tests/Updates/main.swift -o .build/UpdateTests
.build/UpdateTests
# Compilation only: never execute the administrator authorization AppleScript.
/usr/bin/osacompile -o .build/update-tests/authorize.scpt .build/update-tests/authorize.applescript
python3 Scripts/test-updater-command.py
