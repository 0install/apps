#os=Windows
from urllib import request
import re
from datetime import datetime

data = request.urlopen('https://www.python.org/downloads/windows/').read().decode('utf-8')

releases = []
for match in re.findall(r'Python (3)\.([0-9]+)\.([0-9]+)([0-9abrc]+?) - (.*)<\/a>', data):
    version_major = match[0]
    version_minor = match[1]
    version_patch = match[2]
    version_suffix = match[3]

    version_main = version_major + "." + version_minor + "." + version_patch
    version_full = version_main + version_suffix
    if not (version_full + "-embed-arm64.zip") in data:
        continue

    if version_suffix.startswith('rc'):
        stability = 'testing'
        version = version_main + "-" + version_suffix
    elif version_suffix.startswith('b'):
        stability = 'developer'
        version = version_main + "-" + version_suffix.replace("b", "pre")
    elif version_suffix.startswith('a'):
        stability = 'developer'
        version = version_main + "-" + version_suffix.replace("a", "pre-pre")
    elif version_suffix != "":
        continue
    else:
        stability = 'stable'
        version = version_main

    try:
        released_parsed = datetime.strptime(match[4].replace('Sept.', 'Sep.'), '%b. %d, %Y')
    except ValueError:
        released_parsed = datetime.strptime(match[4], '%B %d, %Y')
    released = datetime.strftime(released_parsed, '%Y-%m-%d')

    releases.append({
        'version': version,
        'version-full': version_full,
        'version-main': version_main,
        'version-minor': version_minor,
        'stability': stability,
        'released': released
    })
