#os=Windows
import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import github


releases = [{
    'version-original': release['tag_name'].strip('jq-'),
    'version': release['tag_name'].strip('jq-').replace('rc', '-rc'),
    'stability': 'testing' if release['prerelease'] else 'stable',
    'released': release['published_at'][0:10]
} for release in github.releases('stedolan/jq') if len(release['assets']) > 0]
