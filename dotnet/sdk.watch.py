#os=Linux
from urllib import request
import json

def get_releases(channel):
    data = request.urlopen('https://builds.dotnet.microsoft.com/dotnet/release-metadata/' + channel + '/releases.json').read().decode('utf-8')
    return [{
        'version': release['sdk']['version'],
        'released': release['release-date']
    } for release in json.loads(data)['releases'] if not '-' in release['release-version']]

releases = get_releases('8.0') + get_releases('9.0')
