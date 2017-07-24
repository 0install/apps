from urllib import request
import re

def find_matches(uri):
    data = request.urlopen(uri).read()
    return re.findall(r'>docker-([0-9\.\-cerc]+).zip<\/a>\s*(....-..-..)', data.decode())

def convert(match, channel):
    return {'version': match[0].replace('-ce', ''),
        'version-original': match[0],
        'stability': 'testing' if channel == 'edge' else 'stable',
        'channel': channel,
        'released': match[1]
    }

matches_stable = find_matches('https://download.docker.com/win/static/stable/x86_64/')
matches_edge = find_matches('https://download.docker.com/win/static/edge/x86_64/')

releases = [convert(match, 'stable') for match in matches_stable] + [convert(match, 'edge') for match in matches_edge if match not in matches_stable]
