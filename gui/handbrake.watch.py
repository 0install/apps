import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import github

releases = []

for release in github.releases('HandBrake/HandBrake'):
    if release['prerelease']:
        continue
    version = release['tag_name']
    asset_name = 'HandBrake-' + version + '-x86_64-Win_GUI.zip'
    if any(asset['name'] == asset_name for asset in release['assets']):
        releases.append({
            'version': version,
            'released': release['published_at'][0:10]
        })
