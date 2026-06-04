#!/usr/bin/env python3
"""Run a 0install ``.watch.py`` script standalone and print the releases it produces.

This is the fast inner loop for developing a watch script. It executes the script
exactly the way 0watch does -- with the script's own directory as ``__file__``'s
location, so the usual ``sys.path.insert(0, '..')`` line makes repo-root helpers
(such as ``github``) importable -- then prints the resulting ``releases``
list as JSON. It does NOT download archives or generate feeds, so it's cheap to
re-run while you iterate on parsing/normalization.

Usage:
    python3 run_watch.py path/to/name.watch.py

Set GITHUB_TOKEN in the environment first if the script hits GitHub and you're
getting rate-limited.
"""
import json
import os
import runpy
import sys


def main(argv):
    if len(argv) != 2:
        sys.exit(f"usage: {os.path.basename(argv[0])} path/to/name.watch.py")

    watch_path = os.path.abspath(argv[1])
    if not os.path.isfile(watch_path):
        sys.exit(f"no such file: {watch_path}")

    # run_name="__main__" + the absolute path mean dirname(__file__) inside the
    # script resolves to the real category directory, matching how 0watch runs it.
    namespace = runpy.run_path(watch_path, run_name="__main__")

    releases = namespace.get("releases")
    if releases is None:
        sys.exit("the script did not define a `releases` variable")
    if not isinstance(releases, list):
        sys.exit(f"`releases` is {type(releases).__name__}, expected a list of dicts")

    print(json.dumps(releases, indent=2, default=str))
    print(f"\n{len(releases)} release(s)", file=sys.stderr)


if __name__ == "__main__":
    main(sys.argv)
