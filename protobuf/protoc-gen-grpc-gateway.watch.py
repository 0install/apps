from urllib import request
import json
import re

data = request.urlopen('https://api.github.com/repos/grpc-ecosystem/grpc-gateway/releases').read().decode('utf-8')
releases = [{
    'version': release['tag_name'].strip('v'),
    'released': release['published_at'][0:10]
} for release in json.loads(data) if not 'alpha' in release['tag_name'] and not 'beta' in release['tag_name'] and not 'rc' in release['tag_name'] and len(release['assets']) > 0]
