from urllib import request
import json

excluded_versions = ['v1.8.0', 'v2.1.0-unsupported.20180809']

def convert(release):
    return {
        'version': release['tag_name'][1:].replace('beta.', 'pre'),
        'version-original': release['tag_name'][1:],
        'stability': 'testing' if release['prerelease'] else 'stable',
        'released': release['published_at'][0:10]
    }

data = request.urlopen('https://api.github.com/repos/electron/electron/releases').read().decode('utf-8')
releases = [convert(release) for release in json.loads(data) if not release['tag_name'] in excluded_versions]
