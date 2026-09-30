#!/bin/bash
set -euo pipefail
cd "$(dirname "$0")/.."
mkdir -p .build/module-cache
xcrun swiftc -swift-version 5 -module-cache-path .build/module-cache Sources/Shared/Protocol.swift Sources/Shared/SessionEngine.swift Sources/Shared/SafetyPolicy.swift Tests/main.swift -o .build/AlwaysAwakeTests
.build/AlwaysAwakeTests
plutil -lint Resources/Info.plist Resources/com.alwaysawake.mac.helper.plist
xcrun swiftc -swift-version 5 -module-cache-path .build/module-cache Sources/Shared/Protocol.swift Sources/Control/LocalControl.swift Sources/MCP/MCPServer.swift Tests/MCP/main.swift -o .build/MCPTests
.build/MCPTests
xcrun swiftc -swift-version 5 -module-cache-path .build/module-cache Sources/Shared/Protocol.swift Sources/Shared/SafetyPolicy.swift Sources/Control/LocalControl.swift Sources/App/AutomationControl.swift Tests/Automation/main.swift -o .build/AutomationTests
.build/AutomationTests
xcrun swiftc -swift-version 5 -module-cache-path .build/module-cache Sources/Shared/Protocol.swift Sources/Shared/SessionEngine.swift Sources/Shared/SleepSetting.swift Tests/SleepSetting/main.swift -o .build/SleepSettingTests
.build/SleepSettingTests
