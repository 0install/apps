#os=Windows
from urllib import request
import gzip, re
from datetime import datetime

bytes = request.urlopen('https://www.python.org/downloads/windows/').read()

# Response is sometimes, but not always, GZip-compressed
try: bytes = gzip.decompress(bytes)
except: pass

data = bytes.decode('utf-8')

releases = []
for match in re.findall(r'Python (3)\.([0-9]+)\.([0-9]+)([0-9abrc]*?) - (.*)<\/a>', data):
    version_suffix = match[3]
    version_minor_part = match[1]
    version_patch = match[0] + "." + version_minor_part + "." + match[2]
    version_full = version_patch + version_suffix

    if not (version_full + "-embed-arm64.zip") in data:
        continue

    if version_suffix.startswith('rc'):
        stability = 'testing'
        version = version_patch + "-" + version_suffix
    #elif version_suffix.startswith('b'):
    #    stability = 'developer'
    #    version = version_patch + "-" + version_suffix.replace("b", "pre")
    #elif version_suffix.startswith('a'):
    #    stability = 'developer'
    #    version = version_patch + "-" + version_suffix.replace("a", "pre-pre")
    elif version_suffix != "":
        continue
    else:
        stability = 'stable'
        version = version_patch

    try:
        released_parsed = datetime.strptime(match[4].replace('Sept.', 'Sep.'), '%b. %d, %Y')
    except ValueError:
        released_parsed = datetime.strptime(match[4], '%B %d, %Y')
    released = datetime.strftime(released_parsed, '%Y-%m-%d')

    releases.append({
        'version': version,
        'version-full': version_full,
        'version-patch': version_patch,
        'version-minor-part': version_minor_part,
        'stability': stability,
        'released': released
    })
