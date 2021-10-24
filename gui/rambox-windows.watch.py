#os=Windows
import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import github

releases = [{
    'version': release['tag_name'],
    'released': release['published_at'][0:10]
} for release in github.releases('ramboxapp/community-edition') if not release['tag_name'] in ('0.5.2', '0.5.3', '0.5.9')]
