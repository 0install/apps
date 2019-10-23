from urllib import request
import json

def convert(release):
    version = release['tag_name'].strip('v')
    released = release['published_at'][0:10]
    return {'version': version, 'released': released}

data = request.urlopen('https://api.github.com/repos/atom/atom/releases').read().decode('utf-8')
releases = [convert(release) for release in json.loads(data) if not release['prerelease'] and not 'beta' in release['tag_name']]
