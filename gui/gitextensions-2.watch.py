from urllib import request
import json

def convert(release):
    original_version = release['tag_name'].strip('v')
    version = original_version.replace('.0', '.').replace('beta', 'pre').replace('.RC', '-rc').replace('RC', '-rc')
    stability = 'testing' if 'rc' in version or 'beta' in version else 'stable'
    released = release['published_at'][0:10]
    return {'version': version, 'original-version': original_version, 'stability': stability, 'released': released}

data = request.urlopen('https://api.github.com/repos/gitextensions/gitextensions/releases').read().decode('utf-8')
releases = [convert(release) for release in json.loads(data) if str.startswith(release['tag_name'], 'v2.') and len(release['assets']) > 0]
