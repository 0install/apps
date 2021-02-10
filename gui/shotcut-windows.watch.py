#os=Windows
import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from github import releases

releases = [{
    'tag': release['tag_name'],
    'version': release['tag_name'].strip('v').replace('.0', '.'),
    'date': release['tag_name'].strip('v').replace('.', ''),
    'stability': 'testing' if release['prerelease'] else 'stable',
    'released': release['published_at'][0:10]
} for release in releases('mltframework/shotcut') if not 'UNSTABLE' in release['name']]
