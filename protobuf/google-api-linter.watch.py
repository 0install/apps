import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import github

excluded_versions = ['v1.36.0']

releases = [{
    'version': release['tag_name'].strip('v'),
    'released': release['published_at'][0:10]
} for release in github.releases('googleapis/api-linter') if not release['tag_name'] in excluded_versions]
