import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import github

releases = [{
    'version': release['tag_name'],
    'stability': 'testing' if release['prerelease'] else 'stable',
    'released': release['published_at'][0:10]
} for release in github.releases('docker/compose') if release['tag_name'][0:2] == '1.' and release['tag_name'] != '1.25.2-rc1']
