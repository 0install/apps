# Icon reference

Icons are the one asset CI never generates. They live only on the **`gh-pages`** branch (the `public/` checkout next to `feeds/`), never on `master`, and feeds reference them by their published URL.

Do this actively; don't leave it to the user. If the project has no icon anywhere you can find, ship with **no `<icon>` element at all** and skip the rest.

## 1. Find source images

Look in the **upstream project's own Git repo** first: logos usually sit at the repo root or under `assets/`, `images/` or `docs/`. Take a `.png` or `.svg` for the primary icon, **plus any ready-made `.ico` or `.icns` the project already ships**. Prefer a square, transparent-background PNG between 128px and 512px.

## 2. Produce the formats the feed needs

Name each file exactly after the feed:

| File | When |
| --- | --- |
| `name.png` | **Required** whenever the feed has any icon. |
| `name.ico` | Only for cross-platform or Windows-only feeds (Windows uses it for shortcuts). |
| `name.icns` | Only for cross-platform or macOS-only **GUI** feeds. Skip it for CLI tools. |

Prefer a `.ico`/`.icns` the project already ships over generating one; they are usually better tuned. Otherwise:

- **`.svg` → `.png`**: rasterize first (`magick -background none logo.svg -resize 256x256 name.png`).
- **`.png` → `.ico`**: `magick name.png -define icon:auto-resize=256,48,32,16 name.ico`.
- **`.png` → `.icns`**: **do not use `magick`.** `magick name.png name.icns` exits successfully but writes a PNG with an `.icns` extension. Use `iconutil` on macOS or `png2icns` (libicns) on Linux. If neither is available and upstream ships no `.icns`, leave the `.icns` out rather than publishing a mislabelled file.

If `magick` (ImageMagick) isn't installed, prefix the command with `0install run https://apps.0install.net/utils/imagemagick.xml` in place of `magick`.

## 3. Place the files

Copy each file to `../public/CATEGORY/name.<ext>` (relative to the `feeds/` checkout). Check that the checkout is the right branch first:

```bash
git -C ../public rev-parse --abbrev-ref HEAD
```

It must print `gh-pages`.

**Stop there: don't commit or push in `public/`.** That checkout is otherwise CI output, and a push to `gh-pages` goes live immediately. Tell the user which icon files are waiting in `../public/CATEGORY/` so they can commit and push them.

## 4. Reference them in the feed

Add one `<icon>` line per format you produced, in **both** the template and the seed master feed:

```xml
<icon href="https://apps.0install.net/CATEGORY/name.png" type="image/png"/>
<icon href="https://apps.0install.net/CATEGORY/name.ico" type="image/vnd.microsoft.icon"/>
<icon href="https://apps.0install.net/CATEGORY/name.icns" type="image/x-icns"/>
```

Until the files are pushed to `gh-pages` the URLs return 404. feedlint then reports `ERROR ... HTTP error: got status code 404` / `ERRORS FOUND: 1` for the icon. A lone icon 404 is expected at that stage and is not a defect in the feed.
