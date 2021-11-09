from urllib import request
import json

def get_releases(channel):
    data = request.urlopen('https://raw.githubusercontent.com/dotnet/core/master/release-notes/' + channel + '/releases.json').read().decode('utf-8')
    return [{
        'version': release['aspnetcore-runtime']['version'],
        'released': release['release-date']
    } for release in json.loads(data)['releases'] if not '-' in release['release-version'] and 'aspnetcore-runtime' in release]

releases = get_releases('5.0') + get_releases('6.0')
