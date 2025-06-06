import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import github

releases = [{
    'version': release['tag_name'].strip('v'),
    'released':  release['published_at'][0:10]
} for release in github.releases('cli/cli') if not release['prerelease'] and any(asset['label'].endswith('windows arm64') for asset in release['assets'])]
