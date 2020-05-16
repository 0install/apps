from urllib import request
import json

data = request.urlopen('https://api.github.com/repos/NickeManarin/ScreenToGif/releases').read().decode('utf-8')
releases = [{'version': release['tag_name'], 'released': release['published_at'][0:10]} for release in json.loads(data) if release['assets']]
