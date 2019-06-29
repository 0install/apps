from urllib import request
import json

def convert(release):
    return {
        'version-original': release['tag_name'].strip('jq-'),
        'version': release['tag_name'].strip('jq-').replace('rc', '-rc'),
        'stability': 'testing' if release['prerelease'] else 'stable',
        'released': release['published_at'][0:10]
    }

data = request.urlopen('https://api.github.com/repos/stedolan/jq/releases').read().decode('utf-8')
releases = [convert(release) for release in json.loads(data) if len(release['assets']) > 0]
