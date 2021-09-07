import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import github

def convert(release):
    tag = release['tag_name']
    version = tag.strip('v').replace('rc.', 'rc').replace('rc', '-rc').replace('--', '-')
    archive_version = version.replace('rc', 'rc-')
    stability = 'testing' if release['prerelease'] else 'stable'
    released = release['published_at'][0:10]
    return {'tag': tag, 'version': version, 'archive-version': archive_version, 'stability': stability, 'released': released}

releases = [convert(release) for release in github.releases('protocolbuffers/protobuf') if any(str.startswith(asset['name'], 'protoc-') for asset in release['assets'])]
