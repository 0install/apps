#os=Darwin
import sys, os, re
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import github

releases = []

for release in github.releases('sqlitebrowser/sqlitebrowser'):
    for asset in release['assets']:
        asset_match = re.match(r'DB\.Browser\.for\.SQLite-v[\d\.]+\.dmg', asset['name'])
        if asset_match:
            releases.append({
                'version': release['tag_name'].strip('v'),
                'stability': 'testing' if release['prerelease'] else 'stable',
                'released': release['published_at'][0:10]
            })
            break
