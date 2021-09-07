import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import github

releases = [{
    'original-version': release['tag_name'].strip('v'), 
    'version': release['tag_name'].strip('v').replace('rc.', 'rc').replace('beta.', 'pre-'),
    'stability': 'testing' if release['prerelease'] else 'stable',
    'released': release['published_at'][0:10]
} for release in github.releases('kubernetes-sigs/service-catalog') if not release['tag_name'] in ['v0.1.40']]
