from urllib import request
import json

def convert(release):
    original_version = release['tag_name'].strip('v')
    if 'beta.' in original_version:
        version = original_version.replace('beta.', 'pre')
        stability = 'testing'
    else:
        version = original_version
        stability = 'stable'
    released = release['published_at'][0:10]
    return {'version': version, 'original-version': original_version, 'stability': stability, 'released': released}

data = request.urlopen('https://api.github.com/repos/GitTools/GitVersion/releases').read().decode('utf-8')
releases = [convert(release) for release in json.loads(data) if len(release['assets']) > 0 and not '+' in release['tag_name']]
