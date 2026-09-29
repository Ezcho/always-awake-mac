# DMG presentation

`Scripts/package.sh` creates a 600 × 360 Finder icon view with pika on the left, the Applications shortcut labelled “Drag to Applications” on the right, and a background arrow. No separate installation note is included. Swift renders the background, CoreServices creates the native alias consumed by Finder, and Python writes `.DS_Store`; packaging does not automate Finder or modify/re-sign the source app.

Pinned Python dependencies install only under `.build/dmg-python` on first use. The build briefly mounts its writable image inside `.build`, saves volume-relative background metadata, detaches it, and converts it to a verified compressed image. It then mounts the image read-only at a different path and checks that Foundation can still resolve the background alias before accepting the package.

Normal build:

```sh
Scripts/package.sh
```

Repackage an existing signed app without changing its contents or creating a zip:

```sh
Scripts/package.sh --app '/path/to/Always Awake.app' --version 1.0.3 --output-dir .build/dmg-preview --dmg-only
```

The explicit version must match the app's `CFBundleShortVersionString`. This produces `pika-1.0.3.dmg` and its `.sha256` file. The script writes local artifacts only and never uploads or replaces GitHub release assets.

Finder still reads a legacy AliasRecord in `icvp.backgroundImageAlias`. The native alias creator is intentionally used only during packaging: it includes disk-image volume metadata that a generic local-disk alias lacks. The alias is converted to a Foundation bookmark to test that it still resolves after relocation.

The destination shortcut itself carries the drag instruction, so installation remains clear if a macOS version ignores custom backgrounds. The shortcut still resolves directly to `/Applications`; no instruction document is added.
