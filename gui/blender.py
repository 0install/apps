from urllib import request
import re
from datetime import datetime

def regex(url, pattern):
    return re.findall(pattern, request.urlopen(url).read().decode('utf-8'))

def releases(suffix):
    for minor_version in regex('https://download.blender.org/release/', r'>Blender([\d\.a-z]+)\/<\/a>'):
        for match in regex('https://download.blender.org/release/Blender' + minor_version + '/', r'>blender-([\d\.\-a-z]+)-' + re.escape(suffix) + '<\/a>\s+(..-...-....)'):
            yield {
                'version': match[0],
                'minor-version': minor_version,
                'released': datetime.strftime(datetime.strptime(match[1], '%d-%b-%Y'), '%Y-%m-%d')
            }
