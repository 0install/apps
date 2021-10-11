from urllib import request
import json
import re

data = json.loads(request.urlopen('https://pypi.org/pypi/pywin32/json').read().decode('utf-8'))

releases = []
for version, downloads in data['releases'].items():
    if len(downloads) == 0: continue
    release = {
        'version': version,
        'released': downloads[0]['upload_time'][0:10]
    }
    for download in downloads:
        release[re.findall(r'-(cp\d+m?-win.+)\.', download['url'])[0]] = download['url']
    releases.append(release)
