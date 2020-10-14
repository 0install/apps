from urllib import request
import json

def convert(release):
    tag = release['tag_name']
    version = tag.strip('v').replace('rc.', 'rc').replace('rc', '-rc').replace('--', '-')
    archive_version = version.replace('rc', 'rc-')
    stability = 'testing' if release['prerelease'] else 'stable'
    released = release['published_at'][0:10]
    return {'tag': tag, 'version': version, 'archive-version': archive_version, 'stability': stability, 'released': released}

data = request.urlopen('https://api.github.com/repos/protocolbuffers/protobuf/releases').read().decode('utf-8')
releases = [convert(release) for release in json.loads(data) if any(str.startswith(asset['name'], 'protoc-') for asset in release['assets'])]
