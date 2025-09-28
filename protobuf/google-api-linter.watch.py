import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import github

excluded_versions = ['v1.36.0', 'v1.55.1', 'v2.0.0-beta.3']

releases = [{
    'original-version': release['tag_name'].strip('v'),
    'version': release['tag_name'].strip('v').replace('beta.', 'pre'),
    'stability': 'testing' if release['prerelease'] else 'stable',
    'released': release['published_at'][0:10]
} for release in github.releases('googleapis/api-linter') if not release['tag_name'] in excluded_versions]
