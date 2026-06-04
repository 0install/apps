# Watch-script reference (`name.watch.py`)

A watch script is a Python program that [0watch](https://docs.0install.net/tools/0watch/) executes to discover upstream releases. Read this when the two examples in SKILL.md aren't enough — version normalization, the `#os=` header, GitLab/other sources, or disabling a script.

## Contents

- [The contract](#the-contract)
- [`releases` dict keys](#releases-dict-keys)
- [GitHub via `github.py`](#github-via-githubpy)
- [Web scraping and JSON APIs](#web-scraping-and-json-apis)
- [Version normalization](#version-normalization)
- [The `#os=` header](#the-os-header)
- [Disabling a watch script](#disabling-a-watch-script)
- [How 0watch decides what's new](#how-0watch-decides-whats-new)

## The contract

The script must set a module-level variable `releases` to a list of dicts. Each dict is one release; each key/value becomes a substitution for the matching `{key}` placeholder in `name.xml.template`. The script doesn't print or write anything — 0watch reads the `releases` variable after exec'ing it, then calls 0template for each version not already packaged.

It runs with the watch file's directory as `__file__`'s location, so the standard `sys.path.insert(0, …'..')` makes repo-root helpers (`github`) importable.

## `releases` dict keys

- `version` — **required**, normalized (see below).
- `released` — ISO `YYYY-MM-DD`. Strongly recommended; templates use `{released}`.
- `stability` — `stable` / `testing` / `developer`. Include when you classify prereleases as `testing`; otherwise hard-code `stability="stable"` in the template and omit this key.
- Any custom key your template references, e.g. `version-original` (raw tag for the download URL), `minor-version`, `release-id`, `build`, `main-version`.

Return only releases you can actually package (those with downloadable assets). For a brand-new feed, mind that 0watch would treat *every* reported version as new, since nothing is packaged yet — see [How 0watch decides what's new](#how-0watch-decides-whats-new).

## GitHub via `github.py`

The repo-root `github.py` helper wraps the GitHub REST API and honors `GITHUB_TOKEN` (set it locally to avoid the low unauthenticated rate limit; CI sets it automatically).

```python
import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import github

releases = [{
    'version': release['tag_name'].lstrip('v'),
    'released': release['published_at'][0:10],
    'stability': 'testing' if release['prerelease'] else 'stable',
} for release in github.releases('OWNER/REPO') if release['assets']]
```

- `github.releases(repo)` → the `/releases` list (each has `tag_name`, `published_at`, `prerelease`, `assets`).
- `github.tags(repo)` → the `/tags` list (only `name` + commit; no dates/assets) — use when a project tags but doesn't cut "releases".
- Filter on `release['assets']` (skip releases with no uploaded binaries) and on `not release['prerelease']` if you don't want prereleases, or map prereleases to `stability: 'testing'`.
- To require a specific asset exists before packaging: `any(a['name'].endswith('linux_arm64.tar.gz') for a in release['assets'])`.

Models: `devel/github-cli.watch.py`, `utils/jq.watch.py`, `devel/cloc.watch.py`.

There is **no `gitlab.py` helper** in this repo. For GitLab or other forges, scrape the API directly with `urllib` (the GitLab releases API is `https://gitlab.com/api/v4/projects/<id>/releases`).

## Web scraping and JSON APIs

Use the stdlib — `urllib.request`, `re`, `json`, `datetime`. No third-party deps.

```python
from urllib import request
import re
from datetime import datetime

data = request.urlopen('https://curl.se/changes.html').read().decode('utf-8')
matches = re.findall(r'Fixed in (\d+\.\d+\.\d+) - (\w+ \d+ \d+)', data)
releases = [{
    'version': m[0],
    'released': datetime.strptime(m[1], '%B %d %Y').strftime('%Y-%m-%d'),
} for m in matches if int(m[1][-4:]) >= 2023]   # bound the scrape to recent releases
```

For JSON APIs (PyPI `https://pypi.org/pypi/<pkg>/json`, Google Cloud Storage listings, etc.) `json.loads(request.urlopen(url).read())` and pick out version + upload date. Bound scrapers to recent versions so you don't regenerate the entire history. Models: `utils/curl.watch.py`, `devel/cmake.watch.py`, `python/pywin32.watch.py`.

When a request needs headers (e.g. a `User-Agent` or auth token), wrap it: `request.urlopen(request.Request(url, headers={...}))`.

## Version normalization

0install versions are dotted lists with optional modifiers: digits/dots, with `-pre`/`-rc`/`-post` separated by `-`. So `1.2.3`, `1.2.3-rc1`, `1.2-post2` are valid; `v1.2.3`, `1.2.3rc1`, `1.2.3a` are **not**. Normalize in the watch script:

- Strip prefixes: `tag.lstrip('v')`, or `tag.removeprefix('name-')` / `tag.strip('jq-')`.
- Insert the modifier dash: `'1.7rc1'` → `'1.7-rc1'` (e.g. `.replace('rc', '-rc')`).
- If the **download URL** still needs the raw tag, keep it as a separate key: `'version-original': tag` and use `{version-original}` in the template's `href`.

The full version grammar is in the [feed specification](https://docs.0install.net/specifications/feed/).

## The `#os=` header

An optional first-line comment `#os=VALUE` pins the script to a single OS. The reason is archive **extraction**, not the script itself: 0watch calls 0template, which downloads *and unpacks* every archive to compute its `manifest-digest`, and 0install can only unpack some archive formats on certain platforms. So the script has to run on an OS where 0template can unpack the formats your template references.

- `.dmg` (Apple disk image) unpacks only on **macOS** → `#os=Darwin`.
- `.msi` unpacks only on **Windows** → `#os=Windows`.
- Plain `.tar.gz` / `.tar.bz2` / `.tar.xz` / `.zip` unpack anywhere → **no header needed**.

If one template mixes formats, pin to the OS that can handle the most restrictive one — e.g. `devel/cmake.xml.template` ships `.tar.gz` for Linux/macOS but an `.msi` for Windows, so its watch script is `#os=Windows` (Windows unpacks the `.tar.gz` too). If a template would need *two* mutually exclusive formats (a `.dmg` and an `.msi`), no single OS can generate it — split it into per-OS feeds instead. That's why many `gui/` apps come as `foo-linux` / `foo-macos` / `foo-windows` trios, each with its own template, watch script and `#os=` header.

Models: `gui/blender-macos.watch.py` (`#os=Darwin`, `.dmg`), `devel/cmake.watch.py` (`#os=Windows`, `.msi`).

## Disabling a watch script

Rename it from `name.watch.py` to `name.watch_.py` (trailing underscore before `.py`). The `*.watch.py` glob in `watch.sh`/`watch.ps1` no longer matches it, so it stops running while staying in the tree for reference. Used for scripts whose upstream broke or that need a rewrite. Examples: `utils/fixparts.watch_.py`, `gui/winscp.watch_.py`.

## How 0watch decides what's new

0watch packages a reported release (calls 0template) **unless** `name.xml` already contains that version, or a `name-VERSION.xml` already sits in the directory. This dedup is what lets it run repeatedly and only generate genuinely new feeds.

Bootstrapping a new package starts by hand-creating the master `name.xml` (SKILL.md step 6): it mirrors the `.xml.template` but with **no `<implementation>` elements**, and the feed URI goes in the `uri` attribute of the top-level `<interface>` (where the template uses `<feed-for interface="…"/>`). Since that fresh master has no implementations, the first 0watch run treats every version your script reports as new and generates them all — which is exactly how the feed gets its initial versions; 0repo then merges them into the master.
