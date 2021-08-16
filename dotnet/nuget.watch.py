from urllib import request
import json

data = request.urlopen('https://dist.nuget.org/index.json?_=1532084851900').read().decode('utf-8')
artifacts = json.loads(data)['artifacts'][0]['versions']
releases = [{
    'original-version': artifact['version'].replace('preview.', 'preview'),
    'version': artifact['version'].replace('preview.', 'pre'),
    'released': artifact['releasedate'][0:10],
    'stability': 'testing' if '-' in artifact['version'] else 'stable'
} for artifact in artifacts if artifact['displayName'] == 'nuget.exe']
