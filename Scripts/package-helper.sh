#!/bin/bash
# Creates unsigned native Installer packages; never installs or starts the helper.
set -euo pipefail
cd "$(dirname "$0")/.."
ROOT="$PWD"
APP="$ROOT/dist/pika.app"
VERSION="$(/usr/libexec/PlistBuddy -c 'Print CFBundleShortVersionString' Resources/Info.plist)"
[[ -d "$APP" ]] || { echo 'Run Scripts/build.sh first.' >&2; exit 1; }
[[ "$(/usr/libexec/PlistBuddy -c 'Print CFBundleShortVersionString' "$APP/Contents/Info.plist")" == "$VERSION" ]] || { echo 'Rebuild the app: version mismatch.' >&2; exit 1; }
[[ "$(/usr/libexec/PlistBuddy -c 'Print CFBundleVersion' "$APP/Contents/Info.plist")" == "$(/usr/libexec/PlistBuddy -c 'Print CFBundleVersion' Resources/Info.plist)" ]] || { echo 'Rebuild the app: build number mismatch.' >&2; exit 1; }
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
/usr/bin/pkgbuild --root "$PAYLOAD" --ownership recommended --install-location / --identifier com.alwaysawake.mac.installer --version "$VERSION" --component-plist "$STAGE/components.plist" --scripts "$STAGE/install-scripts" "$STAGE/pika-component.pkg"
/usr/bin/sed "s/@VERSION@/$VERSION/g" Resources/Installer/Distribution.xml > "$STAGE/Distribution.xml"
/usr/bin/productbuild --distribution "$STAGE/Distribution.xml" --resources Resources/Installer/ui --package-path "$STAGE" "$ROOT/dist/pika-$VERSION.pkg"
# DMG users already installed the matching app. Keep that app in place and ask
# Installer to install only the privileged helper, launchd plist and client pin.
mkdir -p "$STAGE/helper-root"
/usr/bin/ditto "$PAYLOAD/Library" "$STAGE/helper-root/Library"
/usr/bin/ditto "$STAGE/install-scripts" "$STAGE/helper-only-scripts"
printf '%s\n' "$REQUIREMENT" > "$STAGE/helper-only-scripts/expected-client.requirement"
/usr/bin/pkgbuild --root "$STAGE/helper-root" --ownership recommended --install-location / --identifier com.alwaysawake.mac.helper-installer --version "$VERSION" --scripts "$STAGE/helper-only-scripts" "$ROOT/dist/pika-helper-$VERSION.pkg"
/usr/bin/pkgbuild --nopayload --identifier com.alwaysawake.mac.helper-uninstaller --version "$VERSION" --scripts "$STAGE/uninstall-scripts" "$ROOT/dist/pika-helper-uninstall-$VERSION.pkg"
(cd dist && /usr/bin/shasum -a 256 "pika-$VERSION.pkg" "pika-helper-$VERSION.pkg" "pika-helper-uninstall-$VERSION.pkg" > SHA256SUMS-pkg.txt)
echo "Created dist/pika-$VERSION.pkg and helper uninstaller. These packages are unsigned; no privileged installation was performed."
