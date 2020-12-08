#os=Darwin
import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from github import releases

releases = [{
    'version': release['tag_name'].strip('v'),
    'version-short': release['tag_name'].strip('v').replace('.', ''),
    'stability': 'testing' if release['prerelease'] else 'stable',
    'released': release['published_at'][0:10]
} for release in releases('mltframework/shotcut') if any(str.startswith(asset['name'], 'shotcut-macos-signed-') for asset in release['assets'])]
