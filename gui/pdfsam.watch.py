import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import github

releases = []
for release in github.releases('torakiki/pdfsam'):
    if release['prerelease']:
        continue
    version = release['tag_name'].lstrip('v')
    if not any(a['name'] == 'pdfsam-basic-%s-linux-x64.tar.gz' % version for a in release['assets']):
        continue
    releases.append({
        'version': version,
        'released': release['published_at'][0:10],
        'stability': 'stable',
    })
