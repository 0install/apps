from urllib import request
import json

excluded_versions = ['v0.14.1']

data = request.urlopen('https://api.github.com/repos/roboll/helmfile/releases').read().decode('utf-8')
releases = [{'version': release['tag_name'].strip('v'), 'released': release['published_at'][0:10]} for release in json.loads(data) if release['tag_name'] not in excluded_versions]
