#os=Windows
from urllib import request
import json

data = request.urlopen('https://api.github.com/repos/oneclick/rubyinstaller2/releases').read().decode('utf-8')
releases = [{'version': release['tag_name'][14:], 'released': release['published_at'][0:10]} for release in json.loads(data) if release['tag_name'][14].isdigit()]