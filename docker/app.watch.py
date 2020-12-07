import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from github import releases

releases = [{
    'version-original': release['tag_name'].strip('v'),
    'version': release['tag_name'].strip('v').replace('beta', 'pre').replace('zeta', 'rc'),
    'stability': 'testing' if release['prerelease'] else 'stable',
    'released': release['published_at'][0:10]
} for release in releases('docker/app') if release['tag_name'][0] == 'v' and len(release['assets']) > 0]
