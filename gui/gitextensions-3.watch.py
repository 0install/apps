#os=Windows
import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import github

def convert(release):
    version = release['tag_name'].strip('v').replace('.0', '.').replace('..', '.0.').replace('RC', 'rc').replace('beta', 'pre')
    stability = 'testing' if 'rc' in version or 'pre' in version else 'stable'
    released = release['published_at'][0:10]
    download_url = next(asset['browser_download_url'] for asset in release['assets'] if str.endswith(asset['name'], '.msi'))
    return {'version': version, 'download-url': download_url, 'stability': stability, 'released': released}

releases = [convert(release) for release in github.releases('gitextensions/gitextensions') if str.startswith(release['tag_name'], 'v3.')]
