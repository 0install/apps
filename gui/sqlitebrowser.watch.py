from urllib import request
import json

data = request.urlopen('https://api.github.com/repos/sqlitebrowser/sqlitebrowser/releases').read().decode('utf-8')
releases = [{
    'version': release['tag_name'].strip('v').replace('beta', 'pre'),
    'original-version': release['tag_name'].strip('v'), 
    'stability': 'testing' if release['prerelease'] else 'stable',
    'released': release['published_at'][0:10]
} for release in json.loads(data) if not 'alpha' in release['tag_name'] and any(str.endswith(asset['name'], '-win64.zip') for asset in release['assets'])]
