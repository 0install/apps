from urllib.request import urlopen, Request
import re
from datetime import datetime

def regex(url, pattern):
    data = urlopen(Request(url, headers={'User-Agent': 'Mozilla'})).read().decode('utf-8')
    return re.findall(pattern, data)

def releases(suffix):
    for minor_version in regex('https://mirrors.iu13.net/blender/release/', r'>Blender([\d\.a-z]+)\/<\/a>'):
        if minor_version.startswith('1.') or minor_version.startswith('2.'): continue
        for match in regex('https://mirrors.iu13.net/blender/release/Blender' + minor_version + '/', r'>blender-([\d\.\-a-z]+)-' + re.escape(suffix) + r'<\/a><\/td><td align="right">(....-..-..)'):
            yield {
                'version': match[0],
                'minor-version': minor_version,
                'released': match[1]
            }
