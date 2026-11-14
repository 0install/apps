---
name: 0install-packaging
description: >-
  Add or change a package for Zero Install (0install) in the apps.0install.net repository: author or
  fix its feed (`.xml`), 0template template (`.xml.template`) and 0watch version-detection script
  (`.watch.py`), then generate and verify the feed with 0template/0watch. Use this whenever the user
  wants to package a new program for 0install / apps.0install.net (e.g. "add ripgrep to 0install",
  "create a feed/template for <project>", "write a watch script for <tool>", "package <X> as a
  0install feed") or to change an existing package there (e.g. "the <tool> watch script is broken",
  "add an arm64 build to <feed>", "upstream changed its archive layout", "re-enable the disabled
  watch script", "add an entry-point / icon to <feed>").
---

# Packaging for apps.0install.net

This repo (apps.0install.net) publishes [Zero Install](https://0install.net/) feeds for software whose
authors don't publish their own. A package is normally **three files you create**; once it's set up,
automation does the repetitive per-release work:

| File | Purpose |
| --- | --- |
| `CATEGORY/name.xml.template` | The feed with `{placeholder}` holes (version, date, …) for 0template to fill. |
| `CATEGORY/name.watch.py`     | A Python script that discovers upstream releases and feeds their values to the template. |
| `CATEGORY/name.xml`          | The master feed. You create it **once** with metadata and a structural skeleton (`<group>`s, `<command>`s) but **no `<implementation>` elements** (step 6); 0repo fills in and grows the implementations. |

A `name.watch_.py` (trailing underscore) is a watch script that has been **disabled**.

Changing an existing package? Read the pipeline below, then go to [Changing an existing package](#changing-an-existing-package).

## The pipeline (understand this before editing anything)

```
name.watch.py ──(0watch finds new versions)──▶ 0template ──▶ name-1.2.3.xml ──(0repo)──▶ name.xml
   discovers releases          fills the template        per-version feed          master feed
```

- **0watch** runs `name.watch.py`, gets a list of releases, and for each version not yet packaged it calls 0template.
- **0template** takes `name.xml.template` + values (e.g. `version=1.2.3`) and writes `name-1.2.3.xml`: it downloads each archive, computes its `manifest-digest`, and fills in `size`/`extract`/`id`.
- **0repo** merges each per-version `name-1.2.3.xml`'s implementation into the master `name.xml` you created (and updates the catalog). The per-version file and the downloaded archive are throwaway intermediates.

So your job is to write a template that produces a correct feed, a watch script that reports releases, and (for a new package) the metadata-only master feed. Then **verify** by running 0template yourself before committing.

## Conventions used below

- **Working directory**: every command runs from the root of this repo (the `feeds/` checkout). `../incoming/` and `../public/` are its siblings in the 0repo working directory.
- **Shell**: commands are written so they work in both bash and PowerShell. Where they can't, both forms are given. Python is `python` on Windows and `python3` on Linux/macOS.
- **Guardrails**:
  - Commit locally; **don't push** unless the user asks. A push to `master` publishes signed feeds to the live site.
  - **Never commit or push in `../public/`.**
  - **Ask before running 0watch or 0repo.** Running 0template and `run_watch.py` on your own is fine.
  - Never edit an existing `<implementation>` in a master feed (its `id`, digests, archives).

## Step 1 — Gather the facts

Find these before writing anything (ask the user only for what you genuinely can't determine):

- **Identity**: name, one-line summary, longer description, homepage, license as an SPDX identifier (`MIT`, `Apache-2.0`, `GPL-3.0-or-later`).
- **Kind**: a runnable **app/tool** (has a `<command name="run">`), or a **library** (no run command; consumed by other feeds via bindings, see `references/templates.md`).
- **Runtime**: a self-contained native binary, or does it need an interpreter/runtime feed (Python, Java/JDK, .NET/CLR, Perl, Node)? Runtimes are pulled in with `<runner>`/`<requires>`, see `references/templates.md`.
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
| `protobuf/` | protobuf/gRPC tools | `rust/` | Rust toolchain |
| `docker/`, `ruby/`, `perl/`, `lua/`, `powershell/`, `ocaml/` | per-ecosystem | `0install/` | 0install's own tools; published by those tools' release CI, not packaged by hand |

**The implementation language is not the category.** A language dir like `java/`, `python/`, or `golang/` is only for things that *extend that ecosystem*: its runtime (JRE/JDK), build tools (Gradle, Maven), or language-specific libraries. A general-purpose application that merely *happens to be written in* Java/Python/Go belongs in `utils/`, `devel/`, or `gui/` by its **function**, with the language pulled in invisibly via a `<runner>`.

When unsure, prefer `devel/` for developer tooling and `utils/` for general utilities. Then confirm it's new:

```bash
ls CATEGORY/name.*
```

Nothing should exist for a genuinely new package.

## Step 3 — Write the template (`CATEGORY/name.xml.template`)

**Always model it on an existing sibling.** Open 1–2 templates in the same category that match your case (same runtime, similar arch coverage) and copy their structure. This keeps conventions consistent and is more reliable than writing from memory. Good models:

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
  <icon href="https://apps.0install.net/CATEGORY/name.png" type="image/png"/> <!-- omit this line if upstream ships no logo -->

  <feed-for interface="https://apps.0install.net/CATEGORY/name.xml"/>

  <group license="MIT">
    <command name="run" path="bin/name"/>
    <implementation arch="Linux-x86_64" version="{version}" released="{released}" stability="stable">
      <manifest-digest/>
      <archive extract="name-{version}-linux-amd64"
               href="https://github.com/OWNER/REPO/releases/download/v{version}/name-{version}-linux-amd64.tar.gz"
               type="application/x-compressed-tar"/>
    </implementation>
    <!-- repeat <implementation> per arch: Linux-{i486,aarch64}, Darwin-{x86_64,aarch64} (use MacOSX-… instead of Darwin-… for GUI tools), Windows-{x86_64,i486,aarch64} -->
  </group>
</interface>
```

Rules that matter:

- **`<feed-for>`** must point at the canonical published URL `https://apps.0install.net/CATEGORY/name.xml`. This is how 0repo merges the per-version feed into the right master. The filename and category must match.
- **Leave `<manifest-digest/>` empty** and add no `id`/`size`. 0template computes them from the downloaded archive.
- **Placeholders** are `{version}` and `{released}` (ISO `YYYY-MM-DD`), plus `{stability}` if the watch script varies it, plus any custom keys your watch script emits (e.g. `{version-original}` when the download URL uses the raw upstream tag but the feed version is normalized, see jq). Template placeholders and watch-script keys must match **exactly**: 0template rejects a `{key}` without a value and a value without a `{key}`.
- **`<archive extract="dir">`** for tarballs/zips: `extract` is the single top-level directory inside the archive (often `name-{version}-platform`). But many archives have **no wrapping directory** (files sit at the root), in which case you **omit `extract` entirely** (the `path` is then just `name`). Don't guess: list the archive with `tar -tf archive` (or `unzip -l`) and look.
- **`<file dest="name" href="…"/>`** for a single downloaded file (a bare binary or `.exe`); add `executable="true"` for a bare Unix binary. An asset whose **filename has no version in it** (e.g. `name-windows-amd64.exe`) is fine as long as the release **tag** is in the URL path (`/download/v{version}/`).
- **Per arch**: one `<implementation arch="OS-CPU">` each. OS-specific commands (different `path`/`.exe`) go in separate top-level `<group>` blocks; don't nest groups.
- **Multiple executables → multiple `<command>`s**, preferably on the `<group>` so the `<implementation>`s inherit them. The **main entry point** is always `name="run"`. When the app has **both a GUI and a non-GUI main entry point**, name them `name="run-gui"` (GUI) and `name="run"` (CLI). Secondary commands conventionally take the binary's own name. `<command>`s live in the **template**; the matching `<entry-point>`s live in the **master feed** only (step 6).

For libraries, runtime feeds (`<runner>`), dependencies (`<requires>`/`<environment>`/`<executable-in-path>`), the full arch-token list, multi-`<group>` layouts and entry-point rules, **read `references/templates.md`**.

## Step 4 — Write the watch script (`CATEGORY/name.watch.py`)

The contract: the script sets a module-level `releases` list of dicts. Each dict is one release; its keys fill the template's `{placeholders}`. Almost always `version` + `released`; add `stability` and any custom keys as needed. All values must be strings, and the list must not be empty.

**GitHub releases** (the common case): use the shared [`github.py`](../../../github.py) helper:

```python
import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import github

releases = [{
    'version': release['tag_name'].removeprefix('v'),
    'released': release['published_at'][0:10],
} for release in github.releases('OWNER/REPO')
   if not release['prerelease'] and release['assets']]
```

`github.releases(repo)` and `github.tags(repo)` hit the GitHub API (honoring `GITHUB_TOKEN`). Filter out prereleases and tags with no usable assets.

**Web scraping / JSON API**: plain `urllib` + `re` (or `json`):

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

Key points (full detail in **`references/watch-scripts.md`**):

- **Normalize versions** to 0install's format: remove a leading `v`/`name-` prefix with `removeprefix` (not `strip`/`lstrip`, which remove characters, not a prefix), and turn `1.7rc1` into `1.7-rc1` (modifiers are `pre`/`rc`/`post`). If the download URL still needs the raw tag, emit it as a separate key like `version-original`.
- **`#os=` first-line header** decides which CI runner generates the feeds. **No header means the Windows runner**, which is right for ordinary `.tar.gz`/`.tar.xz`/`.zip` archives, including Linux and macOS builds. Add a header only when an archive unpacks on just one OS: `.dmg` → `#os=Darwin`, `.msi` → `#os=Windows`, `.deb`/`.rpm`/`.AppImage` → `#os=Linux`. Verify locally on that same OS.

## Step 5 — Generate and verify

Don't commit untested files. Verify in three escalating steps.

**a. Does the watch script produce sane releases?** No downloads, no feed generation:

```bash
python .claude/skills/0install-packaging/scripts/run_watch.py CATEGORY/name.watch.py
```

This runs the script the way 0watch does, prints the `releases` list and checks it: non-empty, string values, valid versions, `YYYY-MM-DD` dates, and keys that match the template's placeholders exactly. Fix every `PROBLEM:` line. (Set `GITHUB_TOKEN` first if you hit GitHub rate limits.)

**b. Generate the feed for one version with 0template.** This is the real test of the template (URLs resolve, archives download, digests and `extract` compute). Take the newest release from step (a) and pass its values:

```bash
0install run https://apps.0install.net/0install/0template.xml --output ../incoming/name-1.2.3.xml CATEGORY/name.xml.template version=1.2.3 released=2024-01-01
```

Supply **every** placeholder the template uses, including custom keys. The archives are downloaded next to the template (the common extensions are git-ignored). If a download 404s or `extract` is wrong, fix the template and rerun.

**c. Lint and test-run the generated feed:**

```bash
0install run https://apps.0install.net/0install/feedlint.xml ../incoming/name-1.2.3.xml
```

```bash
0install select ../incoming/name-1.2.3.xml
```

```bash
0install run ../incoming/name-1.2.3.xml -- --version
```

`select` resolves dependencies without launching; `run` actually starts a CLI tool (skip it for libraries and GUIs). Only the implementations for the OS you are on can be test-run; for the others, check that the archive listing matches `extract` and the `<command>` path.

Two expected feedlint results that are **not** defects in your feed:

- feedlint *crashes* on implementations that use a `<file>` element, with `AttributeError: 'FileSource' object has no attribute 'start_offset'`. It validates the `<archive>` implementations first, so read the output above the traceback, and rely on `0install select`/`run` for `<file>`-based implementations.
- A lone `HTTP error: got status code 404` for the `<icon>` means the icon isn't on `gh-pages` yet (step 6).

**Clean up**: delete the test feed `../incoming/name-1.2.3.xml` and the downloaded archives in `CATEGORY/`. Step 6 regenerates the feed for real.

## Step 6 — Seed the master feed and populate it

**Two branches.** What you author (templates, watch scripts, the **unsigned** master feeds) lives on `master`, checked out as `feeds/`. The **signed** feeds and the icons live on `gh-pages`, checked out as `../public/`, which is what `https://apps.0install.net/` serves.

**a. Write the seed master `CATEGORY/name.xml`.** It mirrors the template with three differences:

- `uri="https://apps.0install.net/CATEGORY/name.xml"` on `<interface>` **instead of** the template's `<feed-for>`.
- The same structural skeleton (the `<group>`s, `<command>`s and any `<runner>`/`<requires>` they carry) but **no `<implementation>` elements**. The skeleton lets 0repo merge all versions into one shared group tree rather than emitting a group per version. You never hand-write `<implementation>`s.
- `<entry-point>`s (next item), which the template must not have.

A per-OS split (`name-linux.xml` etc. under an aggregate `name.xml`) needs an extra `<feed-for>` in each per-OS master; see `references/populating.md`.

**b. Add `<entry-point>`s, in the master feed only.** One per `<command>`, placed after the metadata and **before** the `<group>`s. For a single-command feed this is enough:

```xml
<entry-point binary-name="name" command="run"/>
```

Multi-command feeds give each entry-point its own `<name>`/`<summary>` and a `<needs-terminal/>` per CLI command. Full rules and a worked example are in `references/templates.md`.

**c. Add the icon.** Follow `references/icons.md`: find upstream's logo, produce `name.png` (plus `.ico`/`.icns` where they apply), copy the files to `../public/CATEGORY/`, and reference them in both the template and the master feed. Don't commit in `../public/`; tell the user the files are there. No logo anywhere means no `<icon>` element.

**d. Populate the versions.** Ask the user first, then run 0watch to generate a feed per release into `../incoming/`:

```bash
0install run https://apps.0install.net/0install/0watch.xml --output ../incoming CATEGORY/name.watch.py
```

Before merging, search `../incoming/` for the digest `4OYMIQUY7QOBJGX36TEJS35ZEQT24QPEMSNZGTFESWMRW6CSXBKQ`. It is the digest of an **empty directory** and means a wrong `extract` for that version.

Then merge with 0repo from the parent directory, without signing. bash:

```bash
( cd .. && NO_SIGN=1 0repo )
```

PowerShell:

```powershell
$env:NO_SIGN = '1'; Push-Location ..; 0repo; Pop-Location
```

0watch commonly succeeds for recent versions and then fails on an older release that doesn't fit the current template. **`references/populating.md`** covers that, the empty digest, and flattening the nested groups 0repo may produce.

**e. Finish.** In `feeds/`, the result is the template, the watch script and the populated `name.xml` (0repo commits the merge itself; commit your sources if they aren't in yet). Tell the user:

- which commits exist in `feeds/` and that they are not pushed;
- which commits 0repo made in `../public/` (not to be pushed; CI regenerates the signed feeds);
- which icon files are waiting in `../public/CATEGORY/`.

## Changing an existing package

Start by reading the package's three files and running step 5a to see what the watch script reports today.

| Change | What to edit | Verify |
| --- | --- | --- |
| Watch script broke (upstream moved, changed tag format) | `name.watch.py` | Step 5a; the newest reported version should be newer than the newest in `name.xml`, and older ones should match versions already there. |
| Upstream changed file names, URL or archive layout | `name.xml.template` | Step 5b–c with the newest release. |
| New architecture | Add an `<implementation>` to the template. | Step 5b–c. It applies to **future** versions only: 0watch skips versions already in `name.xml`. |
| Metadata (summary, description, homepage, category, icon) | **Both** the template and `name.xml`; they carry the same metadata. | `0install select CATEGORY/name.xml` |
| Commands or dependencies | The template, and the matching `<group>` skeleton in `name.xml` for future merges. Add `<entry-point>`s for new commands in `name.xml` only. | Step 5b–c. |
| Re-enable a disabled script | Fix `name.watch_.py`, then rename it to `name.watch.py`. | Step 5a (accepts the `.watch_.py` name), then 5b–c. |
| Disable a script | Rename to `name.watch_.py`. | — |

Rules for changes:

- **Don't touch existing `<implementation>`s** in `name.xml` unless the user asks. Published implementations are referenced by digest.
- A template only affects versions generated after the change. Don't try to regenerate versions that are already published.
- An existing `#os=` header is there for a reason; keep it unless you know it is obsolete.
- New versions arrive through the nightly Update workflow once the fix is on `master`, so there is usually no need to run 0watch or 0repo locally for a fix.
