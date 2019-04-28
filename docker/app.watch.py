from urllib import request
import json

def convert(release):
    return {
        'version-original': release['tag_name'].strip('v'),
        'version': release['tag_name'].strip('v').replace('beta', 'pre'),
        'stability': 'testing' if release['prerelease'] else 'stable',
        'released': release['published_at'][0:10]
    }

data = request.urlopen('https://api.github.com/repos/docker/app/releases').read().decode('utf-8')
releases = [convert(release) for release in json.loads(data) if release['tag_name'][0] == 'v']
