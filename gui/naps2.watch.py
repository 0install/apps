from urllib import request
import json

def convert(release):
    original_version = release['tag_name'].strip('v')
    version = original_version.replace('b', '-pre')
    released = release['published_at'][0:10]
    stability = 'testing' if 'b' not in original_version else 'stable'
    return {'version': version, 'original-version': original_version, 'stability': stability, 'released': released}

data = request.urlopen('https://api.github.com/repos/cyanfish/naps2/releases').read().decode('utf-8')
releases = [convert(release) for release in json.loads(data) if release['assets']]
