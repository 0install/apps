import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from github import releases

excluded_versions = ['v1.8.0', 'v2.1.0-unsupported.20180809']

releases = [{
    'version': release['tag_name'][1:].replace('beta.', 'pre'),
    'version-original': release['tag_name'][1:],
    'stability': 'testing' if release['prerelease'] else 'stable',
    'released': release['published_at'][0:10]
} for release in releases('electron/electron') if not release['tag_name'] in excluded_versions]
