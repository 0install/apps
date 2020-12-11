import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from github import releases
import re

releases = [{
    'version': release['tag_name'].strip('v'),
    'released': release['published_at'][0:10],
    'commit': re.search(r'-([0-9a-f]{7})\.', release['assets'][0]['name']).group(1)
} for release in releases('Studio3T/robomongo') if not release['prerelease'] and 'beta' not in release['tag_name'] and release['tag_name'] != 'v1.1.1' and any(str.startswith(asset['name'], 'robo3t') for asset in release['assets'])]
