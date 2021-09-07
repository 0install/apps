import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import github

def convert(release):
    original_version = release['tag_name'].strip('v')
    version = original_version.replace('rc.', 'rc').replace('alpha.', 'pre-pre').replace('beta.', 'pre')
    released = release['published_at'][0:10]
    stability = 'developer' if 'alpha' in original_version else ('testing' if release['prerelease'] else 'stable')
    return {'version': version, 'original-version': original_version, 'stability': stability, 'released': released}

releases = [convert(release) for release in github.releases('helm/helm') if release['tag_name'].startswith('v3.')]
