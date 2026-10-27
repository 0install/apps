#os=Linux
import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import github

releases = [{
    'version': release['tag_name'],
    'released': release['published_at'][0:10]
} for release in github.releases('libjpeg-turbo/libjpeg-turbo') if not release['prerelease'] and any(asset['name'] == 'libjpeg-turbo-official_' + release['tag_name'] + '_arm64.deb' for asset in release['assets'])]
