import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import github

releases = [{
    'version': release['tag_name'].replace('-stable', ''),
    'version-original': release['tag_name'],
    'released': release['published_at'][0:10],
} for release in github.releases('godotengine/godot')
   if not release['prerelease']
   and release['tag_name'].endswith('-stable')
   and release['tag_name'].startswith('4.')
   and release['assets']]