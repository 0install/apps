#os=Windows
import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import github

def convert(release):
    version = release['tag_name'].strip('v').replace('RC', 'rc').replace('beta', 'pre')
    return {
        'version': version,
        'stability': 'testing' if 'rc' in version or 'pre' in version else 'stable',
        'released': release['published_at'][0:10],
        'download-url-x64':  next(asset['browser_download_url'] for asset in release['assets'] if str.startswith(asset['name'], 'GitExtensions-x64')),
        #'download-url-arm64': next((asset['browser_download_url'] for asset in release['assets'] if str.startswith(asset['name'], 'GitExtensions-arm64')), None),
    }

releases = [convert(release) for release in github.releases('gitextensions/gitextensions') if str.startswith(release['tag_name'], 'v6') and not 'alpha' in release['tag_name']]
