from urllib import request
import json

excluded_versions = ['v7.6', 'v7.6.5']

data = request.urlopen('https://api.github.com/repos/notepad-plus-plus/notepad-plus-plus/releases').read().decode('utf-8')
releases = [{'version': release['tag_name'].strip('v'), 'released': release['published_at'][0:10]} for release in json.loads(data) if release['tag_name'] not in excluded_versions]
