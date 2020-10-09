from urllib import request
import json

data = request.urlopen('https://api.github.com/repos/zeebe-io/zeebe/releases').read().decode('utf-8')
releases = [{
    'version-original': release['tag_name'],
    'version': release['tag_name'].replace('alpha', 'pre'),
    'stability': 'testing' if release['prerelease'] else 'stable',
    'released': release['published_at'][0:10]
} for release in json.loads(data) if any(asset['name'] == 'zbctl' for asset in release['assets'])]
