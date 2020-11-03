#os=Windows
from urllib import request
import json

skipped_versions = ['v1.3.70-eap-42']

def convert(release):
    return {
        'version': release['tag_name'][1:].replace('-RC', '-rc').replace('-M', '-rc').replace('-eap', '-pre'),
        'stability': 'testing' if release['prerelease'] else 'stable',
        'released': release['published_at'][0:10],
        'download-url': [asset['browser_download_url'] for asset in release['assets'] if asset['name'].startswith('kotlin-compiler-')][0]
    }

data = request.urlopen('https://api.github.com/repos/JetBrains/kotlin/releases').read().decode('utf-8')
releases = [convert(release) for release in json.loads(data) if not release['tag_name'] in skipped_versions]
