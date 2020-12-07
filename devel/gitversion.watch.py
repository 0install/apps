import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from github import releases

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

releases = [convert(release) for release in releases('GitTools/GitVersion') if len(release['assets']) > 0 and not '+' in release['tag_name']]
