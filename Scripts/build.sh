#!/bin/bash
set -euo pipefail
cd "$(dirname "$0")/.."

ROOT="$PWD"
BUILD="$ROOT/.build"
DESTINATION="$ROOT/dist/pika.app"
IDENTITY="${SIGNING_IDENTITY:--}"
mkdir -p "$BUILD" "$ROOT/dist"
STAGE="$(mktemp -d "$BUILD/app.XXXXXX")"
APP="$STAGE/pika.app"
cleanup() {
    if [[ -d "$STAGE/previous.app" && ! -e "$DESTINATION" ]]; then
        mv "$STAGE/previous.app" "$DESTINATION"
    fi
    rm -rf "$STAGE"
}
trap cleanup EXIT
mkdir -p "$BUILD/module-cache" "$APP/Contents/MacOS" "$APP/Contents/Resources" "$APP/Contents/Library/HelperTools" "$APP/Contents/Library/LaunchDaemons"
cp Resources/Info.plist "$APP/Contents/Info.plist"
cp Resources/com.alwaysawake.mac.helper.plist "$APP/Contents/Library/LaunchDaemons/"
cp Resources/Guide.html "$APP/Contents/Resources/Guide.html"

SDK="$(xcrun --sdk macosx --show-sdk-path)"
SHARED=(Sources/Shared/SleepSetting.swift Sources/Shared/Protocol.swift Sources/Shared/SessionEngine.swift Sources/Shared/Signature.swift Sources/Shared/InstalledHelper.swift Sources/Shared/SafetyPolicy.swift Sources/Shared/HardwareReading.swift)
for ARCH in arm64 x86_64; do
    FLAGS=(-O -swift-version 5 -sdk "$SDK" -target "${ARCH}-apple-macosx13.0" -module-cache-path "$BUILD/module-cache")
    xcrun swiftc "${FLAGS[@]}" "${SHARED[@]}" Sources/Helper/*.swift -o "$BUILD/AlwaysAwakeHelper-$ARCH"
    xcrun swiftc "${FLAGS[@]}" "${SHARED[@]}" Sources/Control/*.swift Sources/App/*.swift -o "$BUILD/AlwaysAwake-$ARCH"
    xcrun swiftc "${FLAGS[@]}" Sources/Shared/Protocol.swift Sources/Control/*.swift Sources/MCP/*.swift -o "$BUILD/pika-mcp-$ARCH"
done
xcrun lipo -create "$BUILD/AlwaysAwake-arm64" "$BUILD/AlwaysAwake-x86_64" -output "$APP/Contents/MacOS/AlwaysAwake"
xcrun lipo -create "$BUILD/AlwaysAwakeHelper-arm64" "$BUILD/AlwaysAwakeHelper-x86_64" -output "$APP/Contents/Library/HelperTools/AlwaysAwakeHelper"
xcrun lipo -create "$BUILD/pika-mcp-arm64" "$BUILD/pika-mcp-x86_64" -output "$APP/Contents/MacOS/pika-mcp"
xcrun swift -module-cache-path "$BUILD/module-cache" Scripts/make-icon.swift "$BUILD/AppIcon.iconset" "$APP/Contents/Resources/AppIcon.icns"

SIGN_FLAGS=(--force --options runtime --sign "$IDENTITY")
if [[ "$IDENTITY" != "-" ]]; then SIGN_FLAGS+=(--timestamp); fi
codesign "${SIGN_FLAGS[@]}" --identifier com.alwaysawake.mac.helper "$APP/Contents/Library/HelperTools/AlwaysAwakeHelper"
codesign "${SIGN_FLAGS[@]}" --identifier com.alwaysawake.mac.mcp "$APP/Contents/MacOS/pika-mcp"
codesign "${SIGN_FLAGS[@]}" "$APP"
codesign --verify --deep --strict --verbose=2 "$APP"
# Never overwrite an executable in place: a running process may still map it.
# A failed compilation or signature check leaves the previous bundle untouched.
if [[ -e "$DESTINATION" ]]; then
    mv "$DESTINATION" "$STAGE/previous.app"
fi
mv "$APP" "$DESTINATION"
echo "Built: $DESTINATION"
