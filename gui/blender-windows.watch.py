#os=Windows
from urllib import request
import re
from datetime import datetime

def regex(url, pattern):
    return re.findall(pattern, request.urlopen(url).read().decode('utf-8'))

def to_zi_version(input):
    if input.endswith('alpha'):
        return input.replace('alpha', 'pre-pre')
    if input.endswith('beta'):
        return input.replace('beta', 'pre')
    if not input[-1].isdigit():
        return input[:-1] + '-' + str(ord(input[-1]) - 96)
    return input

releases = []

for version_main in regex('https://download.blender.org/release/', r'>Blender([\d\.a-z]+)\/<\/a>'):
    for match in regex('https://download.blender.org/release/Blender' + version_main + '/', r'>blender-([\d\.\-a-z]+)-windows64\.zip<\/a>\s+(..-...-....)'):
        releases.append({
            'version': to_zi_version(match[0].replace('-release', '').replace('rc', '-rc')),
            'version-main': version_main,
            'version-full': match[0],
            'stability': 'testing' if 'alpha' in match[0] or 'beta' in match[0] or 'rc' in match[0] else 'stable',
            'released': datetime.strftime(datetime.strptime(match[1], '%d-%b-%Y'), '%Y-%m-%d')
        })
