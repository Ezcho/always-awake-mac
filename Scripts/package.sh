#!/bin/bash
set -euo pipefail
cd "$(dirname "$0")/.."
ROOT="$PWD"
APP="$ROOT/dist/pika.app"
VERSION=""
OUTPUT_DIR="$ROOT/dist"
DMG_ONLY=0
usage() {
    echo 'Usage: Scripts/package.sh [--app /path/to/app] [--version VERSION] [--output-dir DIR] [--dmg-only]'
}
while [[ $# -gt 0 ]]; do
    case "$1" in
        --app|--version|--output-dir)
            [[ $# -ge 2 ]] || { usage >&2; exit 2; }
            case "$1" in
                --app) APP="$2" ;;
                --version) VERSION="$2" ;;
                --output-dir) OUTPUT_DIR="$2" ;;
            esac
            shift 2 ;;
        --dmg-only) DMG_ONLY=1; shift ;;
        --help|-h) usage; exit 0 ;;
        *) usage >&2; exit 2 ;;
    esac
done
[[ -d "$APP" ]] || { echo 'App missing. Run Scripts/build.sh or supply --app.' >&2; exit 1; }
APP="$(cd "$(dirname "$APP")" && pwd)/$(basename "$APP")"
BUILT_VERSION="$(/usr/libexec/PlistBuddy -c 'Print CFBundleShortVersionString' "$APP/Contents/Info.plist")"
if [[ -z "$VERSION" ]]; then
    VERSION="$(/usr/libexec/PlistBuddy -c 'Print CFBundleShortVersionString' Resources/Info.plist)"
fi
[[ "$VERSION" =~ ^[0-9]+\.[0-9]+\.[0-9]+([.-][A-Za-z0-9]+)*$ ]] || { echo 'Invalid package version.' >&2; exit 1; }
[[ "$BUILT_VERSION" == "$VERSION" ]] || { echo "Built app version $BUILT_VERSION differs from package version $VERSION." >&2; exit 1; }
codesign --verify --deep --strict "$APP"
mkdir -p "$ROOT/.build" "$OUTPUT_DIR"
OUTPUT_DIR="$(cd "$OUTPUT_DIR" && pwd)"
DEPS="$ROOT/.build/dmg-python"
# Libraries stay inside this project's build directory; versions are pinned.
if ! PYTHONPATH="$DEPS" python3 -c 'from importlib.metadata import version; assert version("ds_store") == "1.3.3" and version("mac_alias") == "2.2.3"' 2>/dev/null; then
    python3 -m pip install --upgrade --target "$DEPS" -r Resources/DMG/requirements.txt
fi
STAGE="$(mktemp -d "$ROOT/.build/dmg.XXXXXX")"
MOUNT="$STAGE/mount"
MOUNTED=0
cleanup() {
    if [[ "$MOUNTED" == 1 ]]; then
        # Never remove a staging tree if its image could not be detached.
        hdiutil detach "$MOUNT" -quiet || { echo "Image still mounted at $MOUNT; staging preserved." >&2; return; }
    fi
    rm -rf "$STAGE"
}
trap cleanup EXIT
mkdir -p "$STAGE/payload/.background" "$MOUNT" "$ROOT/.build/module-cache"
ditto "$APP" "$STAGE/payload/pika.app"
ln -s /Applications "$STAGE/payload/Drag to Applications"
xcrun swift -module-cache-path "$ROOT/.build/module-cache" Scripts/DMG-background.swift "$STAGE/payload/.background/background.png"
# Build metadata on the real image filesystem so background aliases survive moving the DMG.
hdiutil create -volname pika -fs HFS+ -srcfolder "$STAGE/payload" -format UDRW "$STAGE/writable.dmg" -quiet
hdiutil attach "$STAGE/writable.dmg" -mountpoint "$MOUNT" -nobrowse -noautoopen -quiet
MOUNTED=1
xcrun clang -Wno-deprecated-declarations -framework CoreServices Scripts/DMG-alias.c -o "$STAGE/create-alias"
"$STAGE/create-alias" "$MOUNT/.background/background.png" "$STAGE/background.alias"
PYTHONPATH="$DEPS" python3 Scripts/DMG-layout.py "$MOUNT" "$STAGE/background.alias"
codesign --verify --deep --strict "$MOUNT/pika.app"
hdiutil detach "$MOUNT" -quiet
MOUNTED=0
hdiutil convert "$STAGE/writable.dmg" -format UDZO -imagekey zlib-level=9 -o "$STAGE/pika-$VERSION.dmg" -quiet
hdiutil verify "$STAGE/pika-$VERSION.dmg" -quiet
# Resolve the native background bookmark after mounting at a different path.
MOUNT="$STAGE/verify-mount"
mkdir -p "$MOUNT"
hdiutil attach "$STAGE/pika-$VERSION.dmg" -readonly -nobrowse -noautoopen -mountpoint "$MOUNT" -quiet
MOUNTED=1
xcrun swift -suppress-warnings -module-cache-path "$ROOT/.build/module-cache" Scripts/DMG-bookmark.swift verify-alias "$STAGE/background.alias"
codesign --verify --deep --strict "$MOUNT/pika.app"
hdiutil detach "$MOUNT" -quiet
MOUNTED=0
mv -f "$STAGE/pika-$VERSION.dmg" "$OUTPUT_DIR/pika-$VERSION.dmg"
if [[ "$DMG_ONLY" == 0 ]]; then
    ditto -c -k --sequesterRsrc --keepParent "$STAGE/payload/pika.app" "$OUTPUT_DIR/pika-$VERSION.zip"
    (cd "$OUTPUT_DIR" && shasum -a 256 "pika-$VERSION.dmg" "pika-$VERSION.zip" > SHA256SUMS.txt)
else
    (cd "$OUTPUT_DIR" && shasum -a 256 "pika-$VERSION.dmg" > "pika-$VERSION.dmg.sha256")
fi
echo "Packaged $OUTPUT_DIR/pika-$VERSION.dmg"
