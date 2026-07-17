import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import github

def convert(release):
    version = release['tag_name'].lstrip('v').replace('rc.', 'rc').replace('beta.', 'pre2-').replace('alpha.', 'pre1-')
    stability = 'testing' if release['prerelease'] else 'stable'
    released = release['published_at'][0:10]
    return {'version': version, 'stability': stability, 'released': released}

releases = [convert(release) for release in github.releases('kubernetes-sigs/kind') if release['assets']]
