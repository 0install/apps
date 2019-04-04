from urllib import request
import json

excluded_versions = ['v0.1.40']

def convert(release):
    version = release['tag_name'].strip('v')
    released = release['published_at'][0:10]
    return {'version': version, 'released': released}

data = request.urlopen('https://api.github.com/repos/kubernetes-incubator/service-catalog/releases').read().decode('utf-8')
releases = [convert(release) for release in json.loads(data) if not release['tag_name'] in excluded_versions]
