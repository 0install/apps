from urllib import request
import json

def convert(release):
    version = release['tag_name'].strip('v').replace('rc.', 'rc')
    released = release['published_at'][0:10]
    stability = 'testing' if release['prerelease'] else 'stable'
    return {'version': version, 'stability': stability, 'released': released}

data = request.urlopen('https://api.github.com/repos/kubernetes/helm/releases').read().decode('utf-8')
releases = [convert(release) for release in json.loads(data)]
