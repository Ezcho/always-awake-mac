#!/bin/bash
# Creates unsigned native Installer packages; never installs or starts the helper.
set -euo pipefail
cd "$(dirname "$0")/.."
ROOT="$PWD"
APP="$ROOT/dist/pika.app"
VERSION="$(/usr/libexec/PlistBuddy -c 'Print CFBundleShortVersionString' Resources/Info.plist)"
[[ -d "$APP" ]] || { echo 'Run Scripts/build.sh first.' >&2; exit 1; }
[[ "$(/usr/libexec/PlistBuddy -c 'Print CFBundleShortVersionString' "$APP/Contents/Info.plist")" == "$VERSION" ]] || { echo 'Rebuild the app: version mismatch.' >&2; exit 1; }
[[ "$(/usr/libexec/PlistBuddy -c 'Print CFBundleIdentifier' "$APP/Contents/Info.plist")" == com.alwaysawake.mac ]] || { echo 'Unexpected app identity.' >&2; exit 1; }
/usr/bin/codesign --verify --deep --strict "$APP"
[[ -z "$(/usr/bin/find "$APP" -type l -print -quit)" ]] || { echo 'Symlinks are not allowed in this app payload.' >&2; exit 1; }
mkdir -p "$ROOT/.build" "$ROOT/dist"
STAGE="$(mktemp -d "$ROOT/.build/pkg.XXXXXX")"
trap 'rm -rf "$STAGE"' EXIT
PAYLOAD="$STAGE/root"
mkdir -p "$PAYLOAD/Applications" "$PAYLOAD/Library/PrivilegedHelperTools" "$PAYLOAD/Library/LaunchDaemons" "$PAYLOAD/Library/Application Support/pika"
/usr/bin/ditto "$APP" "$PAYLOAD/Applications/pika.app"
cp "$APP/Contents/Library/HelperTools/AlwaysAwakeHelper" "$PAYLOAD/Library/PrivilegedHelperTools/com.alwaysawake.mac.installed.helper"
cp Resources/Installer/com.alwaysawake.mac.installed.helper.plist "$PAYLOAD/Library/LaunchDaemons/"
DESIGNATED="$(/usr/bin/codesign -d -r- "$APP" 2>&1 | /usr/bin/sed -n 's/^# designated => //p')"
[[ -n "$DESIGNATED" ]] || { echo 'Missing designated requirement.' >&2; exit 1; }
# Parentheses preserve both architecture cdhash alternatives for an ad-hoc build.
REQUIREMENT="identifier \"com.alwaysawake.mac\" and ($DESIGNATED)"
if /usr/bin/codesign -dv "$APP" 2>&1 | /usr/bin/grep -q 'Signature=adhoc'; then
    [[ "$DESIGNATED" == *'cdhash H"'* ]] || { echo 'Ad-hoc client pin must include a cdhash.' >&2; exit 1; }
fi
printf '%s\n' "$REQUIREMENT" > "$PAYLOAD/Library/Application Support/pika/installed-client.requirement"
/usr/bin/codesign --verify --strict -R="$REQUIREMENT" "$PAYLOAD/Applications/pika.app"
find "$PAYLOAD" -type d -exec chmod 755 {} +
chmod 755 "$PAYLOAD/Library/PrivilegedHelperTools/com.alwaysawake.mac.installed.helper"
chmod 644 "$PAYLOAD/Library/LaunchDaemons/com.alwaysawake.mac.installed.helper.plist" "$PAYLOAD/Library/Application Support/pika/installed-client.requirement"
for kind in install uninstall; do
    mkdir -p "$STAGE/$kind-scripts"
    cp "Resources/Installer/$kind/"* "$STAGE/$kind-scripts/"
    cp Resources/Installer/common.sh "$STAGE/$kind-scripts/"
    chmod 755 "$STAGE/$kind-scripts/"*
    /bin/bash -n "$STAGE/$kind-scripts/preinstall"
    /bin/bash -n "$STAGE/$kind-scripts/postinstall"
done
cat > "$STAGE/components.plist" <<'PLIST'
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0"><array><dict>
<key>RootRelativeBundlePath</key><string>Applications/pika.app</string>
<key>BundleIsRelocatable</key><false/>
<key>BundleIsVersionChecked</key><false/>
<key>BundleHasStrictIdentifier</key><true/>
<key>BundleOverwriteAction</key><string>upgrade</string>
</dict></array></plist>
PLIST
/usr/bin/pkgbuild --root "$PAYLOAD" --ownership recommended --install-location / --identifier com.alwaysawake.mac.installer --version "$VERSION" --component-plist "$STAGE/components.plist" --scripts "$STAGE/install-scripts" "$ROOT/dist/pika-$VERSION.pkg"
/usr/bin/pkgbuild --nopayload --identifier com.alwaysawake.mac.helper-uninstaller --version "$VERSION" --scripts "$STAGE/uninstall-scripts" "$ROOT/dist/pika-helper-uninstall-$VERSION.pkg"
(cd dist && /usr/bin/shasum -a 256 "pika-$VERSION.pkg" "pika-helper-uninstall-$VERSION.pkg" > SHA256SUMS-pkg.txt)
echo "Created dist/pika-$VERSION.pkg and helper uninstaller. These packages are unsigned; no privileged installation was performed."
