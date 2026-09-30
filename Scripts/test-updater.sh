#!/bin/bash
set -euo pipefail
cd "$(dirname "$0")/.."
mkdir -p .build/module-cache
xcrun swiftc -swift-version 5 -module-cache-path .build/module-cache Sources/Shared/Protocol.swift Sources/Shared/UpdateRelease.swift Sources/App/UpdateDownload.swift Tests/Updates/main.swift -o .build/UpdateTests
.build/UpdateTests
xcrun swiftc -swift-version 5 -parse-as-library -module-cache-path .build/module-cache Sources/Shared/Protocol.swift Sources/Shared/UpdateRelease.swift Sources/App/UpdateDownload.swift Tests/UpdateDownload/main.swift -o .build/UpdateDownloadTests
.build/UpdateDownloadTests
python3 Scripts/test-update-feed.py
xcrun swiftc -swift-version 5 -parse-as-library -module-cache-path .build/module-cache Sources/Shared/Protocol.swift Sources/Shared/UpdateRelease.swift Sources/App/SystemInstallerHandoff.swift Tests/InstallerHandoff/main.swift -o .build/InstallerHandoffTests
.build/InstallerHandoffTests
