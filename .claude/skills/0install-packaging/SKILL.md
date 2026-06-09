---
name: 0install-packaging
description: >-
  Package a new app, tool, or library for Zero Install (0install) in the apps.0install.net repository —
  authoring its feed (`.xml`), 0template template (`.xml.template`), and 0watch version-detection
  script (`.watch.py`), then generating and verifying the feed with 0template/0watch. Use this whenever
  the user wants to add or package a new program for 0install / apps.0install.net (e.g. "add ripgrep to
  0install", "create a feed/template for <project>", "write a watch script for <tool>", "package <X> as
  a 0install feed").
---

# Adding 0install packages

This repo (apps.0install.net) publishes [Zero Install](https://0install.net/) feeds for software whose
authors don't publish their own. A package is normally **three files you create** — though once it's
set up, automation does the repetitive per-release work:

| File | Purpose |
| --- | --- |
| `CATEGORY/name.xml.template` | The feed with `{placeholder}` holes (version, date, …) for 0template to fill. |
| `CATEGORY/name.watch.py`     | A Python script that discovers upstream releases and feeds their values to the template. |
| `CATEGORY/name.xml`          | The master feed. You create it **once** with metadata and a structural skeleton (`<group>`s, `<command>`s) but **no `<implementation>` elements** (step 6); 0repo fills in and grows the implementations. |

## The pipeline (understand this before editing anything)

```
name.watch.py ──(0watch finds new versions)──▶ 0template ──▶ name-1.2.3.xml ──(0repo)──▶ name.xml
   discovers releases          fills the template        per-version feed          master feed
```

- **0watch** runs `name.watch.py`, gets a list of releases, and for each version not yet packaged it calls 0template.
- **0template** takes `name.xml.template` + values (e.g. `version=1.2.3`) and writes `name-1.2.3.xml`: it downloads each archive, computes its `manifest-digest`, and fills in `size`/`extract`/`id`.
- **0repo** merges each per-version `name-1.2.3.xml`'s implementation into the master `name.xml` you created (and updates the catalog). The per-version file and the downloaded archive are throwaway intermediates.

So your job is to write a template that produces a correct feed, a watch script that reports releases, and — for a new package — the metadata-only master feed. Then **verify** by running 0template/0watch yourself before committing.

## Step 1 — Gather the facts

Find these before writing anything (ask the user only for what you genuinely can't determine):

- **Identity**: name, one-line summary, longer description, homepage, license (SPDX identifier, e.g. `MIT`, `Apache-2.0`).
- **Kind**: a runnable **app/tool** (has a `<command name="run">`), or a **library** (no run command — consumed by other feeds via bindings; see `references/templates.md`).
- **Runtime**: a self-contained native binary, or does it need an interpreter/runtime feed (Python, Java/JDK, .NET/CLR, Perl, Node)? Runtimes are pulled in with `<runner>`/`<requires>` — see `references/templates.md`.
- **Distribution**: where releases live (a GitHub repo's releases/tags is by far the most common; otherwise an upstream downloads/changelog page or a JSON API like PyPI), the exact download-URL pattern, and which OS/arch builds exist.
- **CLI vs GUI**: CLI tools get `<needs-terminal/>`; GUI apps omit it.

## Step 2 — Pick the category and check for duplicates

The directory reflects the **ecosystem the tool belongs to**:

| Dir | Contents | Dir | Contents |
| --- | --- | --- | --- |
| `devel/` | general dev tools, CLIs, SDKs (cmake, terraform, gh) | `gui/` | desktop GUI apps |
| `utils/` | system/shell utilities (curl, jq, ffmpeg) | `lib/` | native shared libraries (no run command) |
| `python/` | Python runtime + Python libs | `java/` | JVM runtimes + build tools |
| `golang/` | Go toolchain + Go tools | `dotnet/` | .NET SDK/runtime + tools |
| `javascript/` | Node/Electron/nwjs | `kubernetes/` | k8s-ecosystem CLIs (helm, k9s) |
| `protobuf/` | protobuf/gRPC tools | `docker/`, `ruby/`, `perl/`, `powershell/`, `ocaml/` | per-ecosystem |

**The implementation language is not the category.** A language dir like `java/`, `python/`, or `golang/` is only for things that *extend that ecosystem* — its runtime (JRE/JDK), build tools (Gradle, Maven), or language-specific libraries. A general-purpose application that merely *happens to be written in* Java/Python/Go belongs in `utils/`, `devel/`, or `gui/` by its **function**, with the language pulled in invisibly via a `<runner>`.

When unsure, prefer `devel/` for developer tooling and `utils/` for general utilities. Then confirm it's new:

```bash
ls CATEGORY/name.*    # nothing should exist for a genuinely new package
```

## Step 3 — Write the template (`CATEGORY/name.xml.template`)

**Always model it on an existing sibling.** Open 1–2 templates in the same category that match your case (same runtime, similar arch coverage) and copy their structure — this keeps conventions consistent and is more reliable than writing from memory. Good models:

- GitHub multi-arch native binary: [`devel/github-cli.xml.template`](../../../devel/github-cli.xml.template)
- single-file-per-arch download: [`utils/jq.xml.template`](../../../utils/jq.xml.template)
- JVM app with a runner: [`java/gradle.xml.template`](../../../java/gradle.xml.template)

Minimal cross-platform skeleton:

```xml
<?xml version="1.0" encoding="utf-8"?>
<interface xmlns="http://zero-install.sourceforge.net/2004/injector/interface">
  <name>Name</name>
  <summary>one line, lowercase start, no trailing period</summary>
  <description>A longer description.</description>
  <homepage>https://example.com/</homepage>
  <category>Development</category>
  <needs-terminal/>
  <icon href="https://apps.0install.net/CATEGORY/name.png" type="image/png"/> <!-- omit this line now if upstream ships no logo -->

  <feed-for interface="https://apps.0install.net/CATEGORY/name.xml"/>

  <group license="MIT License">
    <command name="run" path="bin/name"/>
    <implementation arch="Linux-x86_64" version="{version}" released="{released}" stability="stable">
      <manifest-digest/>
      <archive extract="name-{version}-linux-amd64"
               href="https://github.com/OWNER/REPO/releases/download/v{version}/name-{version}-linux-amd64.tar.gz"
               type="application/x-compressed-tar"/>
    </implementation>
    <!-- repeat <implementation> per arch: Linux-{i486,aarch64}, Darwin-{x86_64,aarch64}, Windows-{x86_64,i486,aarch64} -->
  </group>
</interface>
```

Rules that matter:

- **`<feed-for>`** must point at the canonical published URL `https://apps.0install.net/CATEGORY/name.xml`. This is how 0repo merges the per-version feed into the right master. The filename and category must match.
- **Leave `<manifest-digest/>` empty** and add no `id`/`size`. 0template computes them from the downloaded archive.
- **Placeholders** are `{version}` and `{released}` (ISO `YYYY-MM-DD`), plus `{stability}` if the watch script varies it, plus any custom keys your watch script emits (e.g. `{version-original}` when the download URL uses the raw upstream tag but the feed version is normalized — see jq). Every `{key}` must be supplied by the watch script (or on the 0template command line).
- **`<archive extract="dir">`** for tarballs/zips: `extract` is the single top-level directory inside the archive (often `name-{version}-platform`). But many archives have **no wrapping directory** — files sit at the root — in which case you **omit `extract` entirely** (the `path`/`main` is then just `name`). Don't guess: run `tar -tzf archive.tar.gz` (or `unzip -l`) and look — a single top-level dir → use `extract`; files at root → no `extract`.
- **`<file dest="name" href="…"/>`** for a single downloaded file (a bare binary or `.exe`); add `executable="true"` for a bare Unix binary. Watch for assets whose **filename has no version in it** (e.g. `name-windows-amd64.exe`, identical across releases) — that's fine, because the release **tag** is still in the URL path (`/download/v{version}/`), so `href="…/download/v{version}/name-windows-amd64.exe"` is still version-specific.
- **Per arch**: one `<implementation arch="OS-CPU">` each. OS-specific commands (different `path`/`.exe`) go in separate `<group arch="…">` blocks.
- **Multiple executables → multiple `<command>`s.** An app that ships several runnable binaries gets one `<command>` per binary (preferrably in `<group>`s, so that `<implementation>`s inherit them instead of repeating them). The **main entry point** is always `name="run"`. When the app has **both a GUI and a non-GUI main entry point**, name them `name="run-gui"` (the GUI) and `name="run"` (the CLI) respectively. Secondary commands take a `name` of your choosing — conventionally the binary's own name. The `<command>`s live in the **template** (and thus the generated per-version feeds); the matching `<entry-point>`s live in the **master feed** — see step 6.

For libraries (bindings instead of a run command), runtime feeds (`<runner>`), dependencies (`<requires>`/`<environment>`/`<executable-in-path>`), the full arch-token list, and multi-`<group>` layouts, **read `references/templates.md`**.

## Step 4 — Write the watch script (`CATEGORY/name.watch.py`)

The contract: the script sets a module-level `releases` list of dicts. Each dict is one release; its keys fill the template's `{placeholders}`. Almost always `version` + `released`; add `stability` and any custom keys as needed.

**GitHub releases** (the common case) — use the shared [`github.py`](../../../github.py) helper:

```python
import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import github

releases = [{
    'version': release['tag_name'].lstrip('v'),
    'released': release['published_at'][0:10],
} for release in github.releases('OWNER/REPO')
   if not release['prerelease'] and release['assets']]
```

`github.releases(repo)` and `github.tags(repo)` hit the GitHub API (honoring `GITHUB_TOKEN`). Filter out prereleases and tags with no usable assets.

**Web scraping / JSON API** — plain `urllib` + `re` (or `json`):

```python
from urllib import request
import re
from datetime import datetime

data = request.urlopen('https://example.com/changes.html').read().decode('utf-8')
releases = [{
    'version': m[0],
    'released': datetime.strptime(m[1], '%B %d %Y').strftime('%Y-%m-%d'),
} for m in re.findall(r'Fixed in (\d+\.\d+\.\d+) - (\w+ \d+ \d+)', data)]
```

Key points (full detail, incl. version normalization, the `#os=` header, and disabling a script, in **`references/watch-scripts.md`**):

- **Normalize versions** to 0install's format: strip a leading `v`/`name-` prefix, and turn `1.7rc1` into `1.7-rc1` (modifiers are `pre`/`rc`/`post`). If the download URL still needs the raw tag, emit it as a separate key like `version-original`.
- **`#os=` first-line header**: pin the script to an OS only when an archive can be **extracted** just there. To compute digests, 0template downloads and unpacks every archive, and some formats are OS-specific: `.dmg` unpacks only on macOS (`#os=Darwin`), `.msi` only on Windows (`#os=Windows`). Plain `.tar.gz`/`.zip` unpack anywhere, so they need no header. Full rules in `references/watch-scripts.md`.

## Step 5 — Generate and verify

Don't commit untested files. Verify in three escalating steps.

**a. Fast inner loop — does the watch script produce sane releases?** No downloads, no feed generation:

```bash
python3 .claude/skills/0install-packaging/scripts/run_watch.py CATEGORY/name.watch.py
```

This execs the script the same way 0watch does and prints the `releases` list. Confirm versions are normalized and dates are `YYYY-MM-DD`. (Set `GITHUB_TOKEN` first if you hit GitHub rate limits.)

**b. Generate the feed for one version with 0template** — this is the real test of the template (URLs resolve, archives download, digests/extract compute). Pick the newest version from step (a):

```bash
( cd CATEGORY && 0install run https://apps.0install.net/0install/0template.xml name.xml.template version=1.2.3 released=2024-01-01 )
```

You must supply **every** placeholder the template uses on the command line — at minimum `version=` **and** `released=` (any `YYYY-MM-DD`; it's only a throwaway test feed), plus any custom keys your watch script emits.

It writes `CATEGORY/name-1.2.3.xml` and downloads the archive(s) there. If a download 404s or `extract` is wrong, fix the template and rerun.

**c. Lint and test-run the generated feed:**

```bash
0install run https://apps.0install.net/0install/feedlint.xml CATEGORY/name-1.2.3.xml   # fix warnings
0install select CATEGORY/name-1.2.3.xml      # resolves deps without launching
0install run    CATEGORY/name-1.2.3.xml -- --version   # actually run a CLI tool (skip for libraries/GUIs)
```

**feedlint caveat:** feedlint *crashes* (not warns) on implementations that use a `<file>` element, with `AttributeError: 'FileSource' object has no attribute 'start_offset'`. It validates any `<archive>` implementations first, so you still get useful output above the traceback — that traceback is a feedlint limitation, **not** a defect in your feed. For `<file>`-based implementations (bare binaries / `.exe`), rely on `0install select`/`0install run` to confirm they resolve and launch.

A second expected feedlint result here: if your template carries an `<icon>` whose `gh-pages` file isn't pushed yet, feedlint reports `ERROR ... HTTP error: got status code 404` / `ERRORS FOUND: 1`. That's a hard error, not a warning, but it's harmless — it clears once the icon lands on `gh-pages` (step 6). The archives above it still validate, so treat a lone icon-404 as expected, not a feed defect.

Step b's `0template` run is only a **test**: the `name-1.2.3.xml` it writes is a throwaway for checking the template — you don't commit it. (The real master `name.xml` is the metadata-only file you create in step 6.) Use a single-version `0template` call for this quick test rather than 0watch — running 0watch generates a feed for *every* version your script reports; that bulk population is step 6.

**Clean up**: the downloaded archive (`*.tar.gz`/`*.zip`) is a throwaway — delete it. The per-version `name-1.2.3.xml` is also intermediate; it gets merged by 0repo, so don't commit it.

## Step 6 — Add implementations to the feed

Step 5 only validated the template against one version. Now make the feed live by populating it with every release.

**Two branches.** What you author — templates, watch scripts, and the **unsigned** master feeds — lives on `master`. The **signed** feeds and the icons live on `gh-pages`, which is what `https://apps.0install.net/` serves. The README's **Local setup** clones these as `feeds/` (master) and `public/` (gh-pages).

**Author the sources** (on `master`): `name.xml.template`, `name.watch.py`, and a seed master `name.xml` — the interface metadata identical to the template (`<name>`/`<summary>`/`<description>`/`<homepage>`/`<icon>`/`<category>`) but with `uri="https://apps.0install.net/CATEGORY/name.xml"` on `<interface>` instead of the template's `<feed-for>`. **Mirror the template's structural skeleton** too — the `<group>`(s), `<command>`(s), and any `<runner>`/`<requires>` they carry — **but with no `<implementation>` elements inside them**. Giving 0repo this skeleton up front lets it merge the per-version feeds into a single combined structure (one shared `<group>`/`<command>` tree) rather than emitting a separate group per version. You never hand-write `<implementation>`s — 0template + 0repo produce them.

**Add `<entry-point>`s for every command — in the master feed only, never the template.** Entry-points carry the human-facing metadata (menu name, icon, terminal flag) that desktop integration shows for each command: add one `<entry-point command="…">` per `<command>` the template defines, with `binary-name` when the command's `name` differs from the executable's filename, a repeated `<needs-terminal/>` for each CLI command (omit it for GUI ones), and `<name>`/`<summary>` to give each command a distinct menu label. All three are optional for a single-command feed — a bare `<entry-point binary-name="name" command="run"/>` suffices, since the interface's own `<name>`/`<summary>` already describe it. **See `references/templates.md` for the full rules and a worked multi-command example.**

**Add the icon** (on `gh-pages`) — **do this actively, don't punt it to the user.** Icons are the one asset CI never generates; they live only on `gh-pages`, never on `master`. If the project has no icon anywhere you can find, that's fine — ship with **no `<icon>` element at all** and skip this step. Otherwise work through it:

1. **Find source images.** Look in the **upstream project's own Git repo** first — logos usually sit at the repo root or under `assets/`, `images/`, or `docs/`. Grab whatever's there: a `.png` or `.svg` for the primary icon, **plus any ready-made `.ico` or `.icns` the project already ships**. Prefer a square, transparent-background PNG between 128px and 512px.
2. **Produce the formats the feed actually needs**, named exactly after the feed:
   - `name.png` — **required** whenever the feed has any icon; the primary icon.
   - `name.ico` — **only** for cross-platform or Windows-only feeds (Windows uses it for shortcuts); skip it for a macOS/Linux-only feed.
   - `name.icns` — **only** for cross-platform or macOS-only feeds; skip it for a Windows/Linux-only feed.

   **Prefer a `.ico`/`.icns` the project already ships** (from step 1) over generating one — they're usually better-tuned. Only convert when none exists: rasterize an `.svg` to PNG first if that's all you have, then `magick name.png name.ico` for the `.ico` and `magick name.png name.icns` for the `.icns`. If `magick` (ImageMagick) isn't installed, run it through 0install — prefix the command with `0install run https://apps.0install.net/utils/imagemagick.xml` (e.g. `0install run https://apps.0install.net/utils/imagemagick.xml name.png name.ico`).
3. **Place them in the gh-pages checkout.** The README's local layout clones it as `public/` next to `feeds/`, i.e. **`../public/`** relative to your feeds checkout (verify with `git -C ../public rev-parse --abbrev-ref HEAD` → `gh-pages`). Copy each file to `../public/CATEGORY/name.<ext>`.
4. **Reference each format you produced** with its own `<icon>` line — in **both** the template and the seed master — using the matching MIME type:

   ```xml
   <icon href="https://apps.0install.net/CATEGORY/name.png" type="image/png"/>
   <icon href="https://apps.0install.net/CATEGORY/name.ico" type="image/vnd.microsoft.icon"/>
   <icon href="https://apps.0install.net/CATEGORY/name.icns" type="image/x-icns"/>
   ```
5. **Commit and push `../public` to `gh-pages`** — a separate commit from your `master` push. Until that lands the `<icon>` URLs 404 (which is also why feedlint reports the icon as unreachable before you've pushed).

**Now populate the versions locally with 0watch + 0repo.** This only works if your checkout matches the README's local layout (the `feeds/` + `public/` clones, the `0repo-config.py`/`archives.db` symlinks, an `incoming/` directory). 0watch generates a per-version feed for every release your script reports into `incoming/`; then 0repo merges them into your seed master `name.xml`:

```bash
( cd feeds/CATEGORY && 0install run https://apps.0install.net/0install/0watch.xml --output ../../incoming name.watch.py )
NO_SIGN=1 0repo
```

> **Ask the user for confirmation before running `0watch` or `0repo`.** These download every archive, digest them, and mutate the local 0repo state — don't run them autonomously. (Running `0template` and `run_watch.py` autonomously is fine.)

Then commit and push **only `feeds/`** — the now-populated `name.xml` plus your sources. You don't need to push `public/`: CI regenerates the signed feeds on `gh-pages` from `master`. That's why `NO_SIGN=1` is fine — it just skips signing 0repo's local `public/` output, which you won't push, while the merge into the `master` feed works exactly the same. This can take a while when the script reports many versions, since every archive is downloaded and digested.

**0watch often succeeds for the newest versions, then fails partway down the list.** It walks releases newest-to-oldest, and an older release frequently doesn't match the template you wrote for the *current* one — it may not have published archives for the same architectures, used a different filename/naming convention, lived at a different URL, or shipped a different archive layout. When 0watch hits such a version it errors out (a 404, a missing `extract` dir, etc.).

A practical strategy for getting those older versions in:

1. Note which version 0watch got stuck on. The versions above it are already in `incoming/` — keep them.
2. **Temporarily edit `name.xml.template`** to match that older release's reality (its arch set, URL pattern, `extract` dir, …).
3. Run `0watch` again — it now skips the versions already produced and generates feeds for the older ones the adjusted template fits.
4. Repeat 1–3 if you hit a still-older convention break.
5. **Restore `name.xml.template` to the current-version form** before committing — the template you commit must describe the *latest* release, since that's what CI uses going forward.

**Before running 0repo, check the generated feeds in `incoming/` for the manifest digest `4OYMIQUY7QOBJGX36TEJS35ZEQT24QPEMSNZGTFESWMRW6CSXBKQ`.** This is the digest of an **empty directory**, and almost always means an archive's `extract` value was wrong — 0template extracted a directory that doesn't exist, getting nothing. This commonly happens when the directory structure inside an archive changed between versions. Fix it the same way as a failing 0watch run: delete those particular per-version feeds from `incoming/`, temporarily edit `name.xml.template` to match the correct layout for those versions, run 0watch again to regenerate them, then restore the template to the current-version form.

Then run `NO_SIGN=1 0repo` once to merge everything that accumulated in `incoming/`.

## File-type quick reference

- `name.xml.template` → feed with `{placeholders}`; consumed by 0template. **Write this.**
- `name.watch.py` → sets `releases = [...]`; consumed by 0watch. **Write this.**
- `name.xml` → master feed. **Create it once** with metadata plus the structural skeleton — `<group>`s, `<command>`s, `<runner>`/`<requires>` (`uri=` on `<interface>`, but **no `<implementation>`s**); 0repo fills in and grows the `<implementation>` list inside that skeleton.
- `name.watch_.py` → a watch script **disabled** by the trailing underscore (the `*.watch.py` glob skips it).
