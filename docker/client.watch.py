from urllib import request
import re

def get_versions(os, channel):
    data = request.urlopen('https://download.docker.com/' + os + '/static/' + channel + '/x86_64/').read().decode('utf-8')
    return re.findall(r'docker-([0-9\.]+)\.tgz<\/a>', data)

stable_versions = get_versions('linux', 'stable')
edge_versions = get_versions('linux', 'edge')

releases = []
for version in edge_versions:
    releases.append({
        'version': version.replace('.03.', '.3.').replace('.06.', '.6.').replace('.09.', '.9.'),
        'version-original': version,
        'stability': 'stable' if version in stable_versions else 'testing',
        'channel': 'stable' if version in stable_versions else 'edge'
    })
