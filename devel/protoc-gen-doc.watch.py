from urllib import request
import json
import re

data = request.urlopen('https://api.github.com/repos/pseudomuto/protoc-gen-doc/releases').read().decode('utf-8')
releases = [{
    'version': release['tag_name'].strip('v'),
    'go-version': re.findall(r'go([\d\.]+)\.tar\.gz', release['assets'][0]['name'])[0],
    'released': release['published_at'][0:10]
} for release in json.loads(data) if not release['prerelease'] and '.go' in release['assets'][0]['name']]
