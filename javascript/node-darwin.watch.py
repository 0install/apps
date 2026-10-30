#os=Darwin
from urllib import request
import json

excluded_versions = ['v9.11.0']

def convert(release):
    original_version = release['version'][1:]
    version = original_version.replace('-rc.', '-rc').replace('-beta.', '-pre2-').replace('-alpha.', '-pre1-')
    stability = 'developer' if '-' in original_version else ('stable' if release['lts'] else 'testing')
    return {'version': version, 'original-version': original_version, 'stability': stability, 'released': release['date']}

data = request.urlopen('https://nodejs.org/dist/index.json').read().decode('utf-8')
releases = [convert(release) for release in json.loads(data) if 'osx-x64-tar' in release['files'] and 'osx-arm64-tar' in release['files'] and not release['version'] in excluded_versions]
