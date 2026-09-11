from urllib import request
from xml.etree import ElementTree
import re
from datetime import datetime

BASE = 'https://sourceforge.net/projects/luabinaries'

# The LuaBinaries home page lists every release as a link to its SourceForge directory.
home = request.urlopen('https://luabinaries.sourceforge.net/').read().decode('utf-8')
versions = []
for version in re.findall(r'/files/(\d+\.\d+\.\d+)/', home):
    if version not in versions:
        versions.append(version)

# Releases older than 5.1.5 use a different file naming scheme (lua5_1_4_Win64_bin.zip).
versions = [version for version in versions
            if tuple(int(part) for part in version.split('.')) >= (5, 1, 5)]


def release(version):
    """Returns the release date if this version ships all archives the template needs, else None."""
    feed = request.urlopen('%s/rss?path=/%s&limit=100' % (BASE, version)).read()
    files = {item.findtext('title'): item.findtext('pubDate')
             for item in ElementTree.fromstring(feed).iterfind('./channel/item')}

    dates = []
    for name in ['lua-%s_Win64_bin.zip' % version,
                 'lua-%s_Win32_bin.zip' % version,
                 'lua-%s_Linux515_64_bin.tar.gz' % version]:
        date = files.get('/%s/Tools Executables/%s' % (version, name))
        if date is None: return None  # Not built for all architectures the template covers
        dates.append(datetime.strptime(' '.join(date.split(' ')[1:4]), '%d %b %Y'))
    return max(dates).strftime('%Y-%m-%d')


def suffix(version):
    """The executables are named after the Lua feature version: lua54.exe, wlua54.exe, luac54.exe"""
    feature = '.'.join(version.split('.')[0:2])
    return feature if feature == '5.1' else feature.replace('.', '')  # 5.1 keeps the dot: lua5.1.exe


releases = []
for version in versions:
    released = release(version)
    if released:
        releases.append({
            'version': version,
            'released': released,
            'suffix': suffix(version)
        })
