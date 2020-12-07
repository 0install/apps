import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from github import releases

releases = [{
    'version-original': release['tag_name'],
    'version': release['tag_name'].replace('alpha', 'pre'),
    'stability': 'testing' if release['prerelease'] else 'stable',
    'released': release['published_at'][0:10]
} for release in releases('zeebe-io/zeebe') if any(asset['name'] == 'zbctl' for asset in release['assets'])]
