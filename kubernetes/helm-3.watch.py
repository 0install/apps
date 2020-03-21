from urllib import request
import json

def convert(release):
    original_version = release['tag_name'].strip('v')
    version = original_version.replace('rc.', 'rc').replace('alpha.', 'pre-pre').replace('beta.', 'pre')
    released = release['published_at'][0:10]
    stability = 'developer' if 'alpha' in original_version else ('testing' if release['prerelease'] else 'stable')
    return {'version': version, 'original-version': original_version, 'stability': stability, 'released': released}

data = request.urlopen('https://api.github.com/repos/helm/helm/releases').read().decode('utf-8')
releases = [convert(release) for release in json.loads(data) if release['tag_name'].startswith('v3.')]
