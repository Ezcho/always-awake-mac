#!/bin/bash
set -euo pipefail
cd "$(dirname "$0")/.."
APP="$PWD/dist/Always Awake.app"
VERSION="$(/usr/libexec/PlistBuddy -c 'Print CFBundleShortVersionString' Resources/Info.plist)"
[[ -d "$APP" ]] || { echo 'Run Scripts/build.sh first.' >&2; exit 1; }
codesign --verify --deep --strict "$APP"
STAGE="$(mktemp -d "$PWD/.build/dmg.XXXXXX")"
trap 'rm -rf "$STAGE"' EXIT
ditto "$APP" "$STAGE/Always Awake.app"
ln -s /Applications "$STAGE/Applications"
cp Resources/설치안내.txt "$STAGE/설치안내.txt"
hdiutil create -volname 'Always Awake' -srcfolder "$STAGE" -ov -format UDZO "dist/Always-Awake-$VERSION.dmg"
ditto -c -k --sequesterRsrc --keepParent "$APP" "dist/Always-Awake-$VERSION.zip"
(cd dist && shasum -a 256 "Always-Awake-$VERSION.dmg" "Always-Awake-$VERSION.zip" > SHA256SUMS.txt)
echo "Packaged dist/Always-Awake-$VERSION.dmg"
