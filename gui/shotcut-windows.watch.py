#os=Windows
import sys, os, re
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import github

releases = []

for release in github.releases('mltframework/shotcut'):
    for asset in release['assets']:
        asset_match = re.match(r'shotcut-win64-(\d{6})\.zip', asset['name'])
        if asset_match:
            releases.append({
                'tag': release['tag_name'],
                'version': release['tag_name'].strip('v').replace('.0', '.'),
                'date': asset_match.group(1),
                'stability': 'testing' if release['prerelease'] else 'stable',
                'released': release['published_at'][0:10]
            })
            break
