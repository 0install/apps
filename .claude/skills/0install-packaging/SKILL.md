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
| `CATEGORY/name.xml`          | The master feed. You create it **once**, with the metadata but **no `<implementation>` elements**; 0repo then fills in and grows the implementations from the generated per-version feeds. Edit metadata here, leave implementations to 0repo. |

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

The directory reflects the **ecosystem/runtime**, not what the tool does:

| Dir | Contents | Dir | Contents |
| --- | --- | --- | --- |
| `devel/` | general dev tools, CLIs, SDKs (cmake, terraform, gh) | `gui/` | desktop GUI apps |
| `utils/` | system/shell utilities (curl, jq, ffmpeg) | `lib/` | native shared libraries (no run command) |
| `python/` | Python runtime + Python libs | `java/` | JVM runtimes + build tools |
| `golang/` | Go toolchain + Go tools | `dotnet/` | .NET SDK/runtime + tools |
| `javascript/` | Node/Electron/nwjs | `kubernetes/` | k8s-ecosystem CLIs (helm, k9s) |
| `protobuf/` | protobuf/gRPC tools | `docker/`, `ruby/`, `perl/`, `powershell/`, `ocaml/` | per-ecosystem |

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
  <icon href="https://apps.0install.net/CATEGORY/name.png" type="image/png"/>

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
- **`<archive extract="dir">`** for tarballs/zips: `extract` is the single top-level directory inside the archive (often `name-{version}-platform`). **`<file dest="name" href="…"/>`** for a single downloaded file (a bare binary or `.exe`); add `executable="true"` for a bare Unix binary.
- **Per arch**: one `<implementation arch="OS-CPU">` each. OS-specific commands (different `path`/`.exe`) go in separate `<group arch="…">` blocks.

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
( cd CATEGORY && 0install run https://apps.0install.net/0install/0template.xml name.xml.template version=1.2.3 )
```

It writes `CATEGORY/name-1.2.3.xml` and downloads the archive(s) there. If a download 404s or `extract` is wrong, fix the template and rerun.

**c. Lint and test-run the generated feed:**

```bash
0install run https://apps.0install.net/0install/feedlint.xml CATEGORY/name-1.2.3.xml   # fix warnings
0install select CATEGORY/name-1.2.3.xml      # resolves deps without launching
0install run    CATEGORY/name-1.2.3.xml -- --version   # actually run a CLI tool (skip for libraries/GUIs)
```

Step b's `0template` run is only a **test**: the `name-1.2.3.xml` it writes is a throwaway for checking the template — you don't commit it. (The real master `name.xml` is the metadata-only file you create in step 6, which 0repo then populates.) Use a single-version `0template` call for this quick test rather than 0watch — running 0watch generates a feed for *every* version your script reports; that bulk population is step 6 (done locally or by CI).

**Clean up**: the downloaded archive (`*.tar.gz`/`*.zip`) is a throwaway — delete it. The per-version `name-1.2.3.xml` is also intermediate; it gets merged by 0repo, so don't commit it.

## Step 6 — Add implementations to the feed (locally or via CI)

Step 5 only validated the template against one version. Now make the feed live: do the part both paths share, then pick how the versions get added.

**Two branches.** What you author — templates, watch scripts, and the **unsigned** master feeds — lives on `master`. The **signed** feeds and the icons live on `gh-pages`, which is what `https://apps.0install.net/` serves. The README's **Local setup** clones these as `feeds/` (master) and `public/` (gh-pages).

**Author the sources** (on `master`): `name.xml.template`, `name.watch.py`, and a seed master `name.xml` — the interface metadata with **no `<implementation>` elements**, identical `<name>`/`<summary>`/`<description>`/`<homepage>`/`<icon>`/`<category>` to the template but with `uri="https://apps.0install.net/CATEGORY/name.xml"` on `<interface>` instead of the template's `<feed-for>`. You never hand-write `<implementation>`s — 0template + 0repo produce them.

**Add the icon** (on `gh-pages`): place `name.png` (plus `name.ico` for Windows and `name.icns` for macOS) under `CATEGORY/` in the `public/` clone, then commit and push it to `gh-pages`. The template's `<icon href="https://apps.0install.net/CATEGORY/name.png">` resolves there. CI generates the signed feeds but **not** the icons, so this is the one asset you publish to `gh-pages` by hand; icons never live on `master`.

**Now add the versions — two ways:**

**Path A — populate locally with 0watch + 0repo.** Only works if your checkout matches the README's local layout (the `feeds/` + `public/` clones, the `0repo-config.py`/`archives.db` symlinks, an `incoming/` directory). 0watch generates a per-version feed for every release your script reports into `incoming/`; then 0repo merges them into your seed master `name.xml`:

```bash
( cd feeds/CATEGORY && 0install run https://apps.0install.net/0install/0watch.xml --output ../../incoming name.watch.py )
NO_SIGN=1 0repo
```

Then commit and push **only `feeds/`** — the now-populated `name.xml` plus your sources. You don't need to push `public/`: CI regenerates the signed feeds on `gh-pages` from `master`. That's why `NO_SIGN=1` is fine — it just skips signing 0repo's local `public/` output, which you won't push, while the merge into the `master` feed works exactly the same. This can take a while when the script reports many versions, since every archive is downloaded and digested.

**Path B — let CI populate it.** Commit the seed (empty) master, the template and the watch script to `master`. Once pushed, the nightly **Update** job runs your watch script, generates *all* the reported versions, and opens an "Automatic updates" PR — merging that publishes the populated, signed feed. No local 0repo setup needed, but the feed stays empty until that nightly run lands.

**Either way, CI keeps it current afterwards.** The nightly **Update** job (`.github/workflows/`) runs every watch script on Linux/macOS/Windows, merges new versions with 0repo, and opens "Automatic updates" PRs to `master`; **Publish** deploys the signed feeds to `gh-pages`. For each future release you do nothing — it's the same 0watch→0template→0repo chain, run for you.

## File-type quick reference

- `name.xml.template` → feed with `{placeholders}`; consumed by 0template. **Write this.**
- `name.watch.py` → sets `releases = [...]`; consumed by 0watch. **Write this.**
- `name.xml` → master feed. **Create it once** with metadata only (`uri=` on `<interface>`, no implementations); 0repo fills in and grows the `<implementation>` list. Edit metadata here; leave implementations to 0repo.
- `name.watch_.py` → a watch script **disabled** by the trailing underscore (the `*.watch.py` glob skips it).
