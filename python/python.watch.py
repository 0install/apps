from urllib import request
import re

def convert(match):
    version_full = match[0] # e.g. 3.7.2rc2
    version_minor = version_full[2] # e.g. 7
    if 'rc' in version_full:
        stability = 'testing'
        version = version_full.replace('rc', '-rc') # e.g. 3.7.2-rc2
        version_main = version_full[0:version_full.index('rc')] # e.g. 3.7.2
    else:
        stability = 'stable'
        version = version_full
        version_main = version_full

    released = match[1]
    return {'version': version, 'version-full': version_full, 'version-main': version_main, 'version-minor': version_minor, 'stability': stability, 'released': released}

data = request.urlopen('https://www.python.org/downloads/windows/').read().decode('utf-8')
matches = re.findall(r'Python (3\.[5-9]\.[0-9rc]+) - (....-..-..)', data)
releases = [convert(match) for match in matches]