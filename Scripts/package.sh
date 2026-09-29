#!/bin/bash
set -euo pipefail
cd "$(dirname "$0")/.."
APP="$PWD/dist/pika.app"
VERSION="$(/usr/libexec/PlistBuddy -c 'Print CFBundleShortVersionString' Resources/Info.plist)"
[[ -d "$APP" ]] || { echo 'Run Scripts/build.sh first.' >&2; exit 1; }
BUILT_VERSION="$(/usr/libexec/PlistBuddy -c 'Print CFBundleShortVersionString' "$APP/Contents/Info.plist")"
[[ "$BUILT_VERSION" == "$VERSION" ]] || {
    echo "Built app version $BUILT_VERSION differs from source version $VERSION. Rebuild first." >&2
    exit 1
}
codesign --verify --deep --strict "$APP"
STAGE="$(mktemp -d "$PWD/.build/dmg.XXXXXX")"
trap 'rm -rf "$STAGE"' EXIT
ditto "$APP" "$STAGE/pika.app"
ln -s /Applications "$STAGE/Applications"
cp Resources/설치안내.txt "$STAGE/설치안내.txt"
hdiutil create -volname 'pika' -srcfolder "$STAGE" -ov -format UDZO "dist/pika-$VERSION.dmg"
ditto -c -k --sequesterRsrc --keepParent "$APP" "dist/pika-$VERSION.zip"
(cd dist && shasum -a 256 "pika-$VERSION.dmg" "pika-$VERSION.zip" > SHA256SUMS.txt)
echo "Packaged dist/pika-$VERSION.dmg"
