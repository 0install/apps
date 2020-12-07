import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from github import releases

def convert(release):
    original_version = release['tag_name'].strip('v')
    version = original_version.replace('b', '-pre')
    released = release['published_at'][0:10]
    stability = 'testing' if 'b' in original_version else 'stable'
    return {'version': version, 'original-version': original_version, 'stability': stability, 'released': released}

releases = [convert(release) for release in releases('cyanfish/naps2') if release['assets']]
