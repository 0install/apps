#!/usr/bin/env python3
"""Run a 0install ``.watch.py`` script standalone, print and check its releases.

This is the fast inner loop for developing a watch script. It executes the script
with the script's own directory as ``__file__``'s location, as 0watch does, so the
usual ``sys.path.insert(0, '..')`` line makes repo-root helpers (such as
``github``) importable. It then prints the resulting ``releases`` list as JSON and
checks it for the mistakes 0watch and 0template would fail on:

* ``releases`` is empty (0watch treats that as an error)
* a release has no ``version``, or the version isn't valid 0install syntax
* ``released`` isn't ``YYYY-MM-DD``
* a value isn't a ``str`` (0watch concatenates ``key + '=' + value``)
* the keys don't match the ``{placeholders}`` of the sibling ``.xml.template``
  (0template rejects both missing and unused values)

It does NOT download archives or generate feeds, so it's cheap to re-run while
you iterate on parsing/normalization. Exits 1 if any check fails.

Usage:
    python run_watch.py path/to/name.watch.py      (python3 on Linux/macOS)

A disabled ``name.watch_.py`` is accepted too. Set GITHUB_TOKEN in the
environment first if the script hits GitHub and you're getting rate-limited.
"""
import json
import os
import re
import runpy
import string
import sys
from xml.dom import minidom, Node

# Version := DottedList ("-" Modifier? DottedList?)*, Modifier := pre | rc | post
VERSION_RE = re.compile(r'^\d+(\.\d+)*(-(pre|rc|post)?(\d+(\.\d+)*)?)*$')
DATE_RE = re.compile(r'^\d{4}-\d{2}-\d{2}$')
SUFFIXES = ('.watch.py', '.watch_.py')


def template_placeholders(template_path):
    """Return the {keys} 0template would expand: in attributes and text nodes."""
    keys = set()

    def scan(text):
        if '{' in text:
            for _, field, _, _ in string.Formatter().parse(text):
                if field:
                    keys.add(field)

    def walk(elem):
        for _, value in elem.attributes.items():
            scan(value)
        for child in elem.childNodes:
            if child.nodeType == Node.TEXT_NODE:
                scan(child.data)
            elif child.nodeType == Node.ELEMENT_NODE:
                walk(child)

    walk(minidom.parse(template_path).documentElement)
    return keys


def check(releases, placeholders):
    """Return a list of problem descriptions (empty if everything is fine)."""
    if not releases:
        return ["`releases` is empty: 0watch treats this as an error"]

    problems = []
    for index, release in enumerate(releases):
        if not isinstance(release, dict):
            problems.append(f"releases[{index}] is {type(release).__name__}, expected a dict")
            continue
        label = f"releases[{index}] (version {release.get('version', '?')})"

        for key, value in release.items():
            if not isinstance(value, str):
                problems.append(f"{label}: '{key}' is {type(value).__name__}, must be str")

        version = release.get('version')
        if version is None:
            problems.append(f"{label}: no 'version' key")
        elif isinstance(version, str) and not VERSION_RE.match(version):
            problems.append(f"{label}: '{version}' is not a valid 0install version")

        released = release.get('released')
        if isinstance(released, str) and not DATE_RE.match(released):
            problems.append(f"{label}: released '{released}' is not YYYY-MM-DD")

        if placeholders is not None:
            # 0template falls back to environment variables for missing keys.
            missing = sorted(k for k in placeholders - set(release) if os.getenv(k) is None)
            unused = sorted(set(release) - placeholders)
            if missing:
                problems.append(f"{label}: template placeholders without a value: {', '.join(missing)}")
            if unused:
                problems.append(f"{label}: keys the template doesn't use: {', '.join(unused)}")
    return problems


def main(argv):
    if len(argv) != 2:
        sys.exit(f"usage: {os.path.basename(argv[0])} path/to/name.watch.py")

    watch_path = os.path.abspath(argv[1])
    if not os.path.isfile(watch_path):
        sys.exit(f"no such file: {watch_path}")
    suffix = next((s for s in SUFFIXES if watch_path.endswith(s)), None)
    if suffix is None:
        sys.exit("watch file must be named *.watch.py (or *.watch_.py if disabled)")

    # The absolute path makes dirname(__file__) inside the script resolve to the
    # real category directory, matching how 0watch runs it.
    namespace = runpy.run_path(watch_path, run_name="watch")

    releases = namespace.get("releases")
    if releases is None:
        sys.exit("the script did not define a `releases` variable")
    if not isinstance(releases, list):
        sys.exit(f"`releases` is {type(releases).__name__}, expected a list of dicts")

    print(json.dumps(releases, indent=2, default=str))
    print(f"\n{len(releases)} release(s)", file=sys.stderr)

    template_path = watch_path[:-len(suffix)] + '.xml.template'
    placeholders = None
    if os.path.isfile(template_path):
        placeholders = template_placeholders(template_path)
    else:
        print(f"note: {os.path.basename(template_path)} not found, placeholders not checked", file=sys.stderr)

    problems = check(releases, placeholders)
    # Collapse the same problem repeated for many releases.
    shown = 0
    for problem in problems:
        if shown == 20:
            print(f"... and {len(problems) - shown} more", file=sys.stderr)
            break
        print("PROBLEM: " + problem, file=sys.stderr)
        shown += 1
    if problems:
        sys.exit(1)
    print("checks passed", file=sys.stderr)


if __name__ == "__main__":
    main(sys.argv)
