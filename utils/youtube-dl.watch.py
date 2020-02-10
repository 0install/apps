from urllib import request
import json

data = request.urlopen('https://api.github.com/repos/rg3/youtube-dl/releases').read().decode('utf-8')
releases = [{'version': release['tag_name'].replace('.0', '.'), 'version-original': release['tag_name'], 'released': release['published_at'][0:10]} for release in json.loads(data) if len(release['assets']) > 0]
