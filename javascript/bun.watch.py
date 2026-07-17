import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import github

releases = [{
    'version': release['tag_name'][len('bun-v'):],
    'released': release['published_at'][0:10],
} for release in github.releases('oven-sh/bun')
   if not release['prerelease'] and any(asset['name'] == 'bun-windows-aarch64.zip' for asset in release['assets'])]
