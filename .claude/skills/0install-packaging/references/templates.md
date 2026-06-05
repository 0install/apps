# Template reference (`name.xml.template`)

A template is an ordinary 0install feed with `{placeholder}` holes that [0template](https://docs.0install.net/tools/0template/) fills in. Read this when the minimal skeleton in SKILL.md isn't enough — libraries, runtime-dependent apps, dependencies, or non-trivial arch coverage. **Always also open a real sibling template in the target category and mirror it.**

## Contents

- [Element checklist](#element-checklist)
- [Placeholders](#placeholders)
- [Arch tokens](#arch-tokens)
- [`<archive>` vs `<file>`](#archive-vs-file)
- [Multi-arch layouts: siblings vs groups](#multi-arch-layouts)
- [Multiple commands and entry-points](#multiple-commands-and-entry-points)
- [Libraries (no run command)](#libraries)
- [Runtime feeds: `<runner>`](#runtime-feeds-runner)
- [Dependencies: `<requires>`, `<environment>`, `<executable-in-path>`](#dependencies)
- [What 0template fills in](#what-0template-fills-in)

## Element checklist

Order, top to bottom inside `<interface xmlns="http://zero-install.sourceforge.net/2004/injector/interface">`:

- `<name>` — display name.
- `<summary>` — one line, starts lowercase, no trailing period (e.g. `command-line JSON processor`).
- `<description>` — a paragraph; optional but expected for publishable feeds.
- `<homepage>` — upstream project URL.
- `<category>` — freedesktop menu category (`Development`, `Utility`, `Network`, `Graphics`, …); optional.
- `<needs-terminal/>` — for CLI tools only; **omit for GUI apps**.
- `<icon href="https://apps.0install.net/CATEGORY/name.png" type="image/png"/>` — PNG; GUI apps that get desktop integration may also add an `.ico` (`type="image/vnd.microsoft.icon"`) and an `.icns` (`type="image/x-icns"`) for macOS. The `href` resolves to the **`gh-pages`** branch: the actual `.png`/`.ico`/`.icns` files live under `CATEGORY/` there, not on `master` (see SKILL.md step 6).
- `<feed-for interface="https://apps.0install.net/CATEGORY/name.xml"/>` — **required**; the canonical URL that 0repo merges into. Filename + category must match the file's location.
- `<group …>` … `<implementation …>` — the versions.

`license` is set as an attribute on `<group>` (or on each `<implementation>`). Use a recognizable name like `MIT License`, `Apache License 2.0`, `GNU General Public License, version 3 or later`.

## Placeholders

`{key}` text anywhere in the template is substituted with the value the watch script (or 0template CLI) supplies for that key. Conventionally:

- `{version}` — the 0install-normalized version; goes in `<implementation version="{version}">` and usually in download URLs.
- `{released}` — ISO date `YYYY-MM-DD`; `<implementation released="{released}">`.
- `{stability}` — `stable` / `testing` / `developer`; use `<implementation stability="{stability}">` only if the watch script varies it, otherwise hard-code `stability="stable"`.
- `{version-original}` — the **raw upstream tag** for use in download URLs when it differs from the normalized `{version}` (e.g. `version=1.7.1` but the asset path needs `jq-1.7.1`). See `utils/jq.xml.template`.
- Any other key the watch script emits (e.g. `{minor-version}`, `{release-id}`, `{build}`). Every `{key}` in the template must be provided, or 0template errors.

## Arch tokens

`arch="OS-CPU"`. Common values:

- OS: `Linux`, `Darwin` (macOS — preferred in newer feeds; older ones use `MacOSX`), `Windows`, `POSIX` (any Unix-like, e.g. portable scripts), `*` (any OS).
- CPU: `x86_64`, `i486` (the usual token for 32-bit x86; `i386`/`i586`/`i686` also seen), `aarch64` (64-bit ARM), `armv7l`, `ppc64`, `*` (any CPU).
- `arch="*-*"` — runs anywhere (platform-independent: pure scripts, JARs, .NET DLLs).
- `arch="*-src"` — a source archive to be compiled (rare here; this repo mostly ships binaries).

Examples: `Linux-x86_64`, `Linux-aarch64`, `Darwin-aarch64`, `Windows-x86_64`, `Windows-i486`.

## `<archive>` vs `<file>`

- **`<archive>`** — a `.tar.gz`/`.zip`/etc. that unpacks to a directory tree.
  - `href` — download URL.
  - `extract` — the single top-level directory inside the archive to use as the implementation root (often `name-{version}-platform`). If the archive has exactly one top-level dir, 0template auto-detects it; set it explicitly anyway when the name embeds the version/platform, both to document intent and because auto-detection only works when there's exactly one.
  - `type` — MIME type; usually inferred from the extension. Common: `application/x-compressed-tar` (`.tar.gz`), `application/zip`, `application/x-xz-compressed-tar` (`.tar.xz`).
- **`<file>`** — a single downloaded file, not an archive.
  - `dest` — the filename to store it as (e.g. `jq.exe`, `cloc`).
  - `executable="true"` — set for a bare Unix binary so it's runnable.
  - See `utils/jq.xml.template` (per-arch `<file dest="jq" executable="true" …>`).

The `<command name="run" path="…">` `path` is relative to the implementation root (i.e. relative to the `extract` directory, or the archive/file root).

## Multi-arch layouts

**Sibling implementations in one `<group>`** — when every arch shares the same `<command>` (same relative `path`). Cleanest; preferred. Each arch is one `<implementation arch="…">`. Model: `devel/github-cli.xml.template` (note it uses *two* groups only because Windows runs `bin/gh.exe` while POSIX runs `bin/gh`).

**Multiple `<group arch="…">` blocks** — when the command path or layout differs per OS (e.g. a macOS `.app` bundle vs a Linux `bin/`), or different dependencies per OS. Each group carries its own `<command>`/`<requires>` and one or more implementations.

Shared attributes (`license`, `stability`) and child elements (`<command>`, `<requires>`, `<environment>`) set on an outer `<group>` are inherited by inner groups/implementations — factor common parts outward.

## Multiple commands and entry-points

An app that ships several runnable executables gets one `<command name="…" path="…"/>` per executable. Put them all in the shared `<group>` so every arch inherits them (use per-arch groups only when the `path`/`.exe` differs by OS).

Naming:

- The **main** entry point is always `name="run"`.
- If the app has **both a GUI and a non-GUI main entry point**, name them `name="run-gui"` (GUI) and `name="run"` (CLI).
- Secondary commands take any `name` — conventionally the binary's own name (`<command name="gitk" path="cmd/gitk.exe"/>`).

`<command>`s go in the **template** (so they flow into every generated per-version feed). The matching `<entry-point>`s — the desktop-integration metadata — go in the **master feed** (`name.xml`) and **must not** appear in the template. Place them after the implementation groups, one per command:

```xml
<entry-point binary-name="git" command="run">       <!-- binary-name: command name ≠ executable -->
  <needs-terminal/>                                 <!-- per-command; CLI only -->
  <name>Git</name>
  <summary>command-line interface for Git</summary>
</entry-point>
<entry-point binary-name="git-gui" command="run-gui">  <!-- GUI: no <needs-terminal/> -->
  <name>Git GUI</name>
  <summary>graphical interface for creating Git commits</summary>
</entry-point>
<entry-point command="gitk">                       <!-- name already matches binary → no binary-name -->
  <name>Gitk GUI</name>
  <summary>graphical interface for editing Git commits</summary>
</entry-point>
```

- **`binary-name`** — required whenever a command's `name` differs from the executable filename (so the menu label and PATH entry use the real binary). `run`/`run-gui` essentially always need it; a `command="gitk"` that runs `gitk.exe` does not.
- **`<name>`/`<summary>`** — add them per entry-point for multi-command apps so each command gets a distinct menu label and description. A single-command feed can use a bare `<entry-point binary-name="name" command="run"/>` and rely on the interface's own `<name>`/`<summary>`.

Models: `devel/git-for-windows.xml(.template)` (full `run` + `run-gui` + many secondary commands) and `utils/curl.xml` (single bare entry-point).

## Libraries

A library feed is just a feed **without** `<command name="run">` — it's consumed by other feeds, not launched. The consumer pulls it in via `<requires>` + a binding (see below). Minimal shape:

```xml
<group license="…">
  <implementation arch="*-*" version="{version}" released="{released}" stability="stable">
    <manifest-digest/>
    <archive href="https://example.com/somelib-{version}.tar.gz"/>
  </implementation>
</group>
```

Native libraries (`.so`/`.dll`/`.dylib`) ship one implementation per `arch`.

## Runtime feeds: `<runner>`

When the program isn't a native binary, a `<runner>` inside `<command>` names the interpreter feed; 0install resolves and prepends it, so users don't need a system install.

```xml
<!-- Python script -->
<command name="run" path="mytool.py">
  <runner interface="https://apps.0install.net/python/python.xml">
    <version not-before="3.10"/>
  </runner>
</command>
```

- **Python**: `https://apps.0install.net/python/python.xml`. Use `command="run-gui"` on the runner for GUI apps that shouldn't open a console on Windows, and omit `<needs-terminal/>`.
- **Java**: `<runner command="java" interface="https://apps.0install.net/java/jdk.xml">`; JARs usually also set `<environment insert="lib/*" name="CLASSPATH"/>` (or `insert="name.jar"` for a single JAR). Model: `java/gradle.xml.template`. **Pick `jdk.xml`, not `jre.xml`, for anything needing Java 9+.** `java/jre.xml` only offers a *downloadable* Oracle JRE **8** (plus system-package fallbacks), so a runner against it resolves to Java 8 and a modern JAR dies at launch with `UnsupportedClassVersionError` (class file 55 = Java 11, 52 = Java 8). `java/jdk.xml` pulls a current OpenJDK via `openjdk.xml`, so it satisfies high `not-before` constraints. Always set the floor the JAR actually requires, e.g. `<version not-before="11"/>` (equivalently `version="11.."`); to discover it, generate the feed and run the tool — a class-version error names the minimum.
- **.NET Framework**: `<runner interface="https://apps.0install.net/dotnet/clr.xml"/>` (or `clr-monopath.xml` when `MONO_PATH` matters).
- **Perl**: `<runner interface="https://apps.0install.net/perl/perl.xml"/>`.

Constrain the runner version only as tightly as you actually need (`<version not-before="3"/>` for "any Python 3").

## Dependencies

Inside `<requires interface="…">` (a hard dependency) or with `importance="recommended"` (optional), declare how the dependency is exposed:

- **`<environment name="VAR" insert="subdir" mode="prepend|append|replace"/>`** — prepend/append/replace `VAR` with `<impl>/subdir`. Used for `PATH`, `PYTHONPATH`, `LD_LIBRARY_PATH`/`DYLD_LIBRARY_PATH`, `CLASSPATH`, `MONO_PATH`, `JAVA_HOME`, etc. `insert=""` means the implementation root itself.
- **`<executable-in-path name="tool"/>`** — put a named executable from the dependency on `PATH` (e.g. requiring `cmake` to run during use). `<executable-in-var name="CC"/>` exposes it via a single variable instead.
- **`version="2.0..!3"`** — constrain the dependency's version range (`>=2.0, <3.0`).

Example (build-tool dependency):

```xml
<requires interface="https://apps.0install.net/devel/cmake.xml">
  <executable-in-path name="cmake"/>
</requires>
```

## What 0template fills in

When you run 0template, it (per the [0template docs](https://docs.0install.net/tools/0template/)):

- expands every `{key}`;
- downloads each `<archive>`/`<file>` to the feed's directory (skipping if already present);
- sets `<archive size="…">`;
- sets `extract` to the single top-level directory if there is one and you left it unset;
- sets the implementation `id` to the archive's `sha1new` digest;
- fills empty attributes of `<manifest-digest/>` (adds `sha256new` if it had none).

So leave `<manifest-digest/>` empty and don't write `id`/`size` yourself.
