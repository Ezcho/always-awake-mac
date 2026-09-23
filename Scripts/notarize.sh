#!/bin/bash
set -euo pipefail
cd "$(dirname "$0")/.."
PROFILE="${1:?Usage: Scripts/notarize.sh KEYCHAIN_PROFILE}"
APP="$PWD/dist/Always Awake.app"
codesign -dv "$APP" 2>&1 | grep -q 'Authority=Developer ID Application:' || {
    echo 'Build with a Developer ID Application identity first.' >&2; exit 1;
}
ditto -c -k --sequesterRsrc --keepParent "$APP" .build/notarization.zip
xcrun notarytool submit .build/notarization.zip --keychain-profile "$PROFILE" --wait
xcrun stapler staple "$APP"
xcrun stapler validate "$APP"
Scripts/package.sh
VERSION="$(/usr/libexec/PlistBuddy -c 'Print CFBundleShortVersionString' Resources/Info.plist)"
DMG="dist/Always-Awake-$VERSION.dmg"
xcrun notarytool submit "$DMG" --keychain-profile "$PROFILE" --wait
xcrun stapler staple "$DMG"
xcrun stapler validate "$DMG"
(cd dist && shasum -a 256 "Always-Awake-$VERSION.dmg" "Always-Awake-$VERSION.zip" > SHA256SUMS.txt)
spctl --assess --type execute --verbose=2 "$APP"
