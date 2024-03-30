import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import github

releases = [{
    'version': release['tag_name'].strip('v'),
    'released': release['published_at'][0:10]
} for release in github.releases('hashicorp/vault') if not release['prerelease'] and not '-' in release['tag_name'] and not '+ent' in release['tag_name']]
