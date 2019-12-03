from urllib import request
import json

def get_download_uri(release, suffix):
    return [file['url'] for file in release['runtime']['files'] if file['name'].endswith(suffix)][0]

def get_releases(channel):
    data = request.urlopen('https://raw.githubusercontent.com/dotnet/core/master/release-notes/' + channel + '/releases.json').read().decode('utf-8')
    return [{
        'version': release['runtime']['version'],
        'released': release['release-date'],
        'windows-x64-download-uri': get_download_uri(release, 'win-x64.zip'),
        'windows-x86-download-uri': get_download_uri(release, 'win-x86.zip'),
        'linux-x64-download-uri': get_download_uri(release, 'linux-x64.tar.gz'),
        'macos-x64-download-uri': get_download_uri(release, 'osx-x64.tar.gz')
    } for release in json.loads(data)['releases'] if not '-' in release['release-version'] and 'runtime' in release]

releases = get_releases('2.1') + get_releases('2.2') + get_releases('3.0')
