import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import github

releases = [{
    'version': release['tag_name'],
    'version-packed': release['tag_name'].replace('.', ''),
    'released': release['published_at'][0:10]
} for release in github.releases('ip7z/7zip')
   if not release['prerelease'] and release['assets']]
