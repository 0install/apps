import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import github

releases = [{
    'version': release['tag_name'].lstrip('v'),
    'released':  release['published_at'][0:10]
} for release in github.releases('gohugoio/hugo')
   if not release['prerelease'] and any(asset['name'].endswith('windows-arm64.zip') for asset in release['assets'])]
