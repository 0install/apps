#os=Darwin
import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import github

releases = [{
    'version': release['tag_name'].strip('v').replace('beta', 'pre'),
    'original-version': release['tag_name'].strip('v'), 
    'stability': 'testing' if release['prerelease'] else 'stable',
    'released': release['published_at'][0:10]
} for release in github.releases('sqlitebrowser/sqlitebrowser') if not 'continuous' in release['tag_name'] and not 'alpha' in release['tag_name'] and any(str.endswith(asset['name'], '-win64.zip') for asset in release['assets'])]
