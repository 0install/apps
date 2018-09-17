from urllib import request
import json

def convert(release):
    sem_ver = release['tag_name'].strip('v')
    if 'beta.' in sem_ver:
        version = sem_ver.replace('beta.', 'pre')
        sem_ver_split = sem_ver.split('beta.')
        nuget_ver = sem_ver_split[0] + 'beta' + sem_ver_split[1].zfill(4)
        stability = 'testing'
    else:
        version = sem_ver
        nuget_ver = sem_ver
        stability = 'stable'
    released = release['published_at'][0:10]
    return {'version': version, 'sem-ver': sem_ver, 'nuget-ver': nuget_ver, 'stability': stability, 'released': released}

data = request.urlopen('https://api.github.com/repos/GitTools/GitVersion/releases').read().decode('utf-8')
releases = [convert(release) for release in json.loads(data) if len(release['assets']) > 0 and not '+' in release['tag_name']]
