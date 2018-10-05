from urllib import request
import json

def convert(release):
    return {
        'version': release['tag_name'][1:].replace('-M', '-rc').replace('-eap', '-pre'),
        'stability': 'testing' if release['prerelease'] else 'stable',
        'released': release['published_at'][0:10],
        'download-url': release['assets'][0]['browser_download_url']
    }

data = request.urlopen('https://api.github.com/repos/JetBrains/kotlin/releases').read().decode('utf-8')
releases = [convert(release) for release in json.loads(data)]
