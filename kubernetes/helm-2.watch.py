import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from github import releases

def convert(release):
    original_version = release['tag_name'].strip('v')
    version = original_version.replace('rc.', 'rc')
    released = release['published_at'][0:10]
    stability = 'testing' if release['prerelease'] else 'stable'
    return {'version': version, 'original-version': original_version, 'stability': stability, 'released': released}

releases = [convert(release) for release in releases('helm/helm') if release['tag_name'].startswith('v2.')]
