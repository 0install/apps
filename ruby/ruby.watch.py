#os=Windows
import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import github

releases = [{
    'version': release['tag_name'][14:],
    'released': release['published_at'][0:10]
} for release in github.releases('oneclick/rubyinstaller2') if release['tag_name'][14].isdigit()]