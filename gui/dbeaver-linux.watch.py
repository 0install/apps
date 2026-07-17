import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import github

releases = [{
    'version': release['tag_name'],
    'released': release['published_at'][0:10],
} for release in github.releases('dbeaver/dbeaver')
   if not release['prerelease'] and any(asset['name'].endswith('-linux-x86_64.tar.gz') for asset in release['assets'])]
