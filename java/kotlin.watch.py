#os=Windows
import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from github import releases

releases = [{
    'version': release['tag_name'][1:].replace('-RC', '-rc').replace('-M', '-rc').replace('-eap', '-pre'),
    'stability': 'testing' if release['prerelease'] else 'stable',
    'released': release['published_at'][0:10],
    'download-url': [asset['browser_download_url'] for asset in release['assets'] if asset['name'].startswith('kotlin-compiler-')][0]
} for release in releases('JetBrains/kotlin')]
