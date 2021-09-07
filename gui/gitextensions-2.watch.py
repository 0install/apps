#os=Windows
import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import github

def convert(release):
    original_version = release['tag_name'].strip('v')
    version = original_version.replace('.0', '.').replace('beta', 'pre').replace('.RC', '-rc').replace('RC', '-rc')
    stability = 'testing' if 'rc' in version or 'beta' in version else 'stable'
    released = release['published_at'][0:10]
    return {'version': version, 'original-version': original_version, 'stability': stability, 'released': released}

releases = [convert(release) for release in github.releases('gitextensions/gitextensions') if str.startswith(release['tag_name'], 'v2.') and len(release['assets']) > 0]
