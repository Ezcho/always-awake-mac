# Native helper installer

`Scripts/package-helper.sh` builds three **unsigned** native Installer packages from the already-built `dist/pika.app`. It does not install anything or execute privileged commands.

- `pika-VERSION.pkg` installs `/Applications/pika.app`, its standalone helper, launchd plist, and a root-protected client-signature requirement.
- `pika-helper-VERSION.pkg` installs only the helper, launchd plist and client pin for the matching app already dragged into Applications. Its preflight verifies that app before changing the helper.
- `pika-helper-uninstall-VERSION.pkg` unloads the helper and removes only its three fixed files. It preserves the app and power-recovery data.

The helper must support the installed paths and Mach service before distributing these packages. Rebuild the app after any source change, then rebuild the packages; an ad-hoc signature pins the exact binaries in this release. Do not replace the app with a different build without updating its helper package.

Before installation or removal, turn Session OFF, remove the previous app-managed helper through pika if present, and quit pika. The native Installer requests administrator authorization. The scripts require `SleepDisabled` to be zero and refuse symlink destinations, unsafe ownership, pending recovery, or an active app. An existing installed helper is unloaded with SIGTERM and must exit before its files can be replaced. No script resets global power settings or deletes the recovery journal.

Packages install only on the current startup disk. The installer does not disable Gatekeeper or other macOS protections. Unsigned package acceptance and actual helper execution still need to be tested on the target Mac; creating a package does not prove these will succeed. A Developer ID Installer signature and notarization remain the recommended public distribution route.

The installed paths are:

- `/Library/PrivilegedHelperTools/com.alwaysawake.mac.installed.helper`
- `/Library/LaunchDaemons/com.alwaysawake.mac.installed.helper.plist`
- `/Library/Application Support/pika/installed-client.requirement`

The plist uses `ProgramArguments`, not `BundleProgram`. Apple documents the Installer/LaunchDaemons route and this distinction here: https://developer.apple.com/forums/thread/771162
