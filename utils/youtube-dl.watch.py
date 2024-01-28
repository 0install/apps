import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import github

releases = [{
    'version': release['tag_name'].replace('.0', '.'),
    'version-original': release['tag_name'],
    'released': release['published_at'][0:10]
} for release in github.releases('ytdl-org/youtube-dl') if release['assets']]
