# Populating a feed with versions (0watch + 0repo)

Read this for the details behind SKILL.md step 6: split feeds, older releases that don't fit the template, empty digests, and cleaning up what 0repo merged.

All commands run from the `feeds/` checkout unless stated otherwise. They need the README's local layout: `feeds/` and `public/` side by side, the `0repo-config.py` and `archives.db` symlinks in their parent directory, and an `incoming/` directory there.

## Contents

- [Per-OS split feeds](#per-os-split-feeds)
- [Running 0watch and 0repo](#running-0watch-and-0repo)
- [Older releases that don't fit the template](#older-releases-that-dont-fit-the-template)
- [The empty-directory digest](#the-empty-directory-digest)
- [Flattening nested groups](#flattening-nested-groups)

## Per-OS split feeds

When a package is split into per-OS templates and master feeds (`name-linux.xml`, `name-windows.xml`, `name-macos.xml`) aggregated by a top-level `name.xml` with `<feed arch="…-*" src="…"/>` entries, there are two different `<feed-for>` targets and both are needed:

| File | `<feed-for interface="…">` points at | Purpose |
| --- | --- | --- |
| `name-linux.xml.template` | `…/CATEGORY/name-linux.xml` (its own per-OS feed) | lets 0repo merge the per-version feed into the right master |
| `name-linux.xml` (seed master) | `…/CATEGORY/name.xml` (the aggregate) | lets tools that find the per-OS feed trace it back to the umbrella interface |

In the seed master, place it after `<homepage>` and before the `<group>`s. Models: `gui/drawio.xml` with `gui/drawio-linux.xml` / `-windows` / `-macos`, and `gui/blender.xml`.

## Running 0watch and 0repo

**Ask the user before running either.** 0watch downloads and digests every archive of every reported version; 0repo rewrites `feeds/` and `public/` and commits in both repos.

Generate a per-version feed for every release the script reports:

```bash
0install run https://apps.0install.net/0install/0watch.xml --output ../incoming CATEGORY/name.watch.py
```

Then merge everything in `incoming/` into the master feeds. 0repo runs from the parent directory, with signing disabled. Don't set `GITHUB_TOKEN` for this: with it, 0repo uploads archives to the GitHub release that hosts them.

bash:

```bash
( cd .. && NO_SIGN=1 0repo )
```

PowerShell:

```powershell
$env:NO_SIGN = '1'; Push-Location ..; 0repo; Pop-Location
```

`NO_SIGN=1` only skips signing 0repo's local `public/` output, which never gets pushed; CI regenerates the signed feeds from `master`. The merge into the master feed is the same either way.

Afterwards, report the commits 0repo made in `feeds/` and `public/`. Don't push either.

## Older releases that don't fit the template

0watch walks releases in the order the script reports them (usually newest first) and stops at the first failure. An older release often doesn't match a template written for the current one: fewer architectures, a different file name or URL, a different archive layout. The symptom is a 404 or a missing `extract` directory partway down the list.

1. Note the version 0watch stopped at. The versions before it are already in `incoming/`; keep them.
2. **Temporarily** edit `name.xml.template` to match that older release (arch set, URL pattern, `extract`, …).
3. Run 0watch again. It skips versions that already have a feed in `incoming/` and continues with the older ones.
4. Repeat for each further convention break.
5. **Restore `name.xml.template` to the current-version form** before committing. CI uses the committed template for all future releases.

If the history is long and old versions add little, bound the watch script to recent releases instead (see `watch-scripts.md`).

## The empty-directory digest

Before running 0repo, search the generated feeds in `incoming/` for:

```
4OYMIQUY7QOBJGX36TEJS35ZEQT24QPEMSNZGTFESWMRW6CSXBKQ
```

This is the `sha256new` digest of an **empty directory**. It almost always means `extract` named a directory that doesn't exist in that version's archive, typically because the layout changed between versions.

Fix it like a failing 0watch run: delete the affected per-version feeds from `incoming/`, temporarily adjust the template to the right layout for those versions, run 0watch again, then restore the template.

## Flattening nested groups

When older versions carry different `<command>`s than the seed skeleton (because the template was adjusted for them), 0repo nests them as inner `<group>`s that override the outer `<command>`s. Rewrite those into separate top-level `<group license="…">`s, each with its full set of `<command>`s, to keep the flat layout described in `templates.md`.

Move `<implementation>` elements unchanged while doing this: never alter their `id`, digests or archives. Then check that old versions still resolve:

```bash
0install select --version=OLD CATEGORY/name.xml
```
