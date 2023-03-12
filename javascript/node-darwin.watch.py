#os=Darwin
from urllib import request
import json

excluded_versions = ['v9.11.0']

data = request.urlopen('https://nodejs.org/dist/index.json').read().decode('utf-8')
releases = [{
    'version': release['version'][1:],
    'stability': 'stable' if release['lts'] else 'testing',
    'released': release['date']
} for release in json.loads(data) if 'osx-arm64-tar' in release['files'] and not release['version'] in excluded_versions]
