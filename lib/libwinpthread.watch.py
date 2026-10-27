import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import msys2

def snapshot(release):
    base, _, post = release['version'].partition('-post')
    return base, int(post or 0)

# MSYS2 builds frequent Git snapshots, so only keep the newest one for each upstream version
latest = {}
for release in msys2.releases('libwinpthread'):
    base, post = snapshot(release)
    if base not in latest or post > snapshot(latest[base])[1]:
        latest[base] = release
releases = list(latest.values())
