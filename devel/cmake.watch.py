from urllib import request
import re

releases = []

data = request.urlopen('https://cmake.org/files/').read().decode('utf-8')
for minor_version in re.findall(r'href="v(3\.[0-9]+)', data):
    data = request.urlopen('https://cmake.org/files/v'+ minor_version).read().decode('utf-8')
    for match in re.findall(r'>cmake-([0-9\.\-rc]+)-win64-x64.zip<\/a><\/td><td align="right">(....-..-..)', data):
        releases.append({
            'minor-version': minor_version,
            'version': match[0],
            'released': match[1],
            'stability': 'testing' if 'rc' in match[0] else 'stable'
        })
