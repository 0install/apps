from urllib import request
from xml.etree import ElementTree
import re
from datetime import datetime

# Snapshots built with a newer JDK than the default
JAVA_21 = ['2.2.2-SNAPSHOT', '2.3.0-SNAPSHOT']

feed = request.urlopen('https://sourceforge.net/projects/violet/rss?path=/violetumleditor&limit=100').read()

releases = []
for item in ElementTree.fromstring(feed).iterfind('./channel/item'):
    match = re.fullmatch(r'/violetumleditor/([^/]+)/violetumleditor-\1\.jar', item.findtext('title'))
    if not match: continue
    version = match.group(1)

    # Upstream publishes most builds as Maven snapshots, e.g. 2.3.2-SNAPSHOT
    snapshot = version.endswith('-SNAPSHOT')
    releases.append({
        'version': version.replace('-SNAPSHOT', '-pre'),
        'version-original': version,
        'released': datetime.strptime(' '.join(item.findtext('pubDate').split(' ')[1:4]), '%d %b %Y').strftime('%Y-%m-%d'),
        'stability': 'testing' if snapshot else 'stable',
        'java-version': '21..' if version in JAVA_21 else '17..'
    })
