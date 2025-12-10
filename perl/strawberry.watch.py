#os=Windows
from urllib import request
import json

data = request.urlopen('https://strawberryperl.com/releases.json').read().decode('utf-8')
releases = [{
    'version': release['version'],
    'released': release['date'],
    'download-url': release['edition']['portable']['url']
} for release in json.loads(data) if 'portable' in release['edition']]
