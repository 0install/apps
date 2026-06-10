import sys, os, re
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import github

releases = [{
    'version': release['tag_name'].lstrip('v'),
    'released': release['published_at'][0:10],
} for release in github.releases('neovim/neovim')
   if not release['prerelease']
   and re.match(r'^v\d+\.\d+\.\d+$', release['tag_name'])
   and release['assets']]
