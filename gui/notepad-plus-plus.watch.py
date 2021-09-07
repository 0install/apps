import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import github

excluded_versions = ['v7.6', 'v7.6.5']

releases = [{
    'version': release['tag_name'].strip('v'),
    'released': release['published_at'][0:10]
} for release in github.releases('notepad-plus-plus/notepad-plus-plus') if release['tag_name'] not in excluded_versions]
