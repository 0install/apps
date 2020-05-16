from urllib import request
import json

data = request.urlopen('https://api.github.com/repos/lucasg/Dependencies/releases').read().decode('utf-8')
releases = [{'version': release['tag_name'].strip('v'), 'released': release['published_at'][0:10]} for release in json.loads(data) if len(release['assets']) > 0]
