from urllib import request
import json

def get_releases(channel):
    data = request.urlopen('https://raw.githubusercontent.com/dotnet/core/master/release-notes/' + channel + '/releases.json').read().decode('utf-8')
    return [{
        'version': release['sdk']['version'],
        'released': release['release-date']
    } for release in json.loads(data)['releases'] if not '-' in release['release-version']]

releases = get_releases('2.1') + get_releases('2.2') + get_releases('3.0') + get_releases('3.1')
