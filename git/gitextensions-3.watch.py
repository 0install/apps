from urllib import request
import json

def convert(release):
    version = release['tag_name'].strip('v').replace('.0', '.').replace('beta', 'pre')
    stability = 'testing' if 'rc' in version or 'pre' in version else 'stable'
    released = release['published_at'][0:10]
    download_url = release['assets'][2]['browser_download_url']
    return {'version': version, 'download-url': download_url, 'stability': stability, 'released': released}

data = request.urlopen('https://api.github.com/repos/gitextensions/gitextensions/releases').read().decode('utf-8')
releases = [convert(release) for release in json.loads(data) if str.startswith(release['tag_name'], 'v3.') and len(release['assets']) == 3]
