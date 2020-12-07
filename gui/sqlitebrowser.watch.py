import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from github import releases

releases = [{
    'version': release['tag_name'].strip('v').replace('beta', 'pre'),
    'original-version': release['tag_name'].strip('v'), 
    'stability': 'testing' if release['prerelease'] else 'stable',
    'released': release['published_at'][0:10]
} for release in releases('sqlitebrowser/sqlitebrowser') if not 'alpha' in release['tag_name'] and any(str.endswith(asset['name'], '-win64.zip') for asset in release['assets'])]
