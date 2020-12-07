import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from github import releases

releases = [{
    'version': release['tag_name'].replace('.0', '.'),
    'version-original': release['tag_name'],
    'released': release['published_at'][0:10]
} for release in releases('rg3/youtube-dl') if len(release['assets']) > 0]
