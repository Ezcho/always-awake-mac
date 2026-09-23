#!/bin/bash
set -euo pipefail
cd "$(dirname "$0")/.."

ROOT="$PWD"
APP="$ROOT/dist/Always Awake.app"
BUILD="$ROOT/.build"
IDENTITY="${SIGNING_IDENTITY:--}"
mkdir -p "$BUILD/module-cache" "$APP/Contents/MacOS" "$APP/Contents/Resources" "$APP/Contents/Library/HelperTools" "$APP/Contents/Library/LaunchDaemons"
cp Resources/Info.plist "$APP/Contents/Info.plist"
cp Resources/com.alwaysawake.mac.helper.plist "$APP/Contents/Library/LaunchDaemons/"
cp Resources/Guide.html "$APP/Contents/Resources/Guide.html"

SDK="$(xcrun --sdk macosx --show-sdk-path)"
SHARED=(Sources/Shared/Protocol.swift Sources/Shared/SessionEngine.swift Sources/Shared/Signature.swift Sources/Shared/SafetyPolicy.swift Sources/Shared/HardwareReading.swift)
for ARCH in arm64 x86_64; do
    FLAGS=(-O -swift-version 5 -sdk "$SDK" -target "${ARCH}-apple-macosx13.0" -module-cache-path "$BUILD/module-cache")
    xcrun swiftc "${FLAGS[@]}" "${SHARED[@]}" Sources/Helper/*.swift -o "$BUILD/AlwaysAwakeHelper-$ARCH"
    xcrun swiftc "${FLAGS[@]}" "${SHARED[@]}" Sources/App/*.swift -o "$BUILD/AlwaysAwake-$ARCH"
done
xcrun lipo -create "$BUILD/AlwaysAwake-arm64" "$BUILD/AlwaysAwake-x86_64" -output "$APP/Contents/MacOS/AlwaysAwake"
xcrun lipo -create "$BUILD/AlwaysAwakeHelper-arm64" "$BUILD/AlwaysAwakeHelper-x86_64" -output "$APP/Contents/Library/HelperTools/AlwaysAwakeHelper"
xcrun swift -module-cache-path "$BUILD/module-cache" Scripts/make-icon.swift "$BUILD/AppIcon.iconset" "$APP/Contents/Resources/AppIcon.icns"

SIGN_FLAGS=(--force --options runtime --sign "$IDENTITY")
if [[ "$IDENTITY" != "-" ]]; then SIGN_FLAGS+=(--timestamp); fi
codesign "${SIGN_FLAGS[@]}" --identifier com.alwaysawake.mac.helper "$APP/Contents/Library/HelperTools/AlwaysAwakeHelper"
codesign "${SIGN_FLAGS[@]}" "$APP"
codesign --verify --deep --strict --verbose=2 "$APP"
echo "Built: $APP"
