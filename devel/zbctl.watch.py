import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import github

releases = [{
    'version-original': release['tag_name'],
    'version': release['tag_name'].replace('alpha', 'pre'),
    'stability': 'testing' if release['prerelease'] else 'stable',
    'released': release['published_at'][0:10]
} for release in github.releases('camunda-cloud/zeebe') if any(asset['name'] == 'zbctl' for asset in release['assets'])]
