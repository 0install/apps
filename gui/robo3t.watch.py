from urllib import request
import json
import re

data = request.urlopen('https://api.github.com/repos/Studio3T/robomongo/releases').read().decode('utf-8')
releases = [{
    'version': release['tag_name'].strip('v'),
    'released': release['published_at'][0:10],
    'commit': re.search(r'-([0-9a-f]{7})\.', release['assets'][0]['name']).group(1)
} for release in json.loads(data) if not release['prerelease'] and any(str.startswith(asset['name'], 'robo3t') for asset in release['assets'])]
