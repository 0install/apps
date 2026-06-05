import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import github

releases = [{
    'version': release['tag_name'].lstrip('v'),
    'stability': 'stable',
    'released': release['published_at'][0:10],
} for release in github.releases('plantuml/plantuml')
   if not release['prerelease']
   and any(asset['name'] == 'plantuml-' + release['tag_name'].lstrip('v') + '.jar' for asset in release['assets'])]
