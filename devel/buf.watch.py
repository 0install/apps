from urllib import request
import json

data = request.urlopen('https://api.github.com/repos/bufbuild/buf/releases').read().decode('utf-8')
releases = [{
    'version': release['tag_name'].strip('v'),
    'stability': 'testing' if release['prerelease'] else 'stable',
    'released': release['published_at'][0:10]
} for release in json.loads(data) if any(str.startswith(asset['name'], 'buf-') for asset in release['assets'])]
