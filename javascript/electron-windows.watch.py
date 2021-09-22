#os=Windows
import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import github

excluded_versions = ['v1.8.0', 'v2.1.0-unsupported.20180809']

releases = [{
    'version': release['tag_name'][1:],
    'released': release['published_at'][0:10]
} for release in github.releases('electron/electron') if not release['prerelease'] and not release['tag_name'] in excluded_versions]
