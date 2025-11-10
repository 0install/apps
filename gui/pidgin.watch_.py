from urllib import request
import xml.etree.ElementTree as ET
import re
from datetime import datetime

excluded_versions = ['1.5.1', '2.0.0', '2.0.1', '2.0.2', '2.1.0', '2.1.1', '2.2.0', '2.2.1', '2.2.0', '2.5.9', '2.6.0', '2.13.0', '2.14.11']

data = request.urlopen('https://sourceforge.net/projects/pidgin/rss?path=/Pidgin').read()

releases = []
for item in ET.fromstring(data).find('channel').findall('item'):
    match = re.search(r'([0-9\.]+)-win32', item.find('title').text)
    if match and match.group(1) not in excluded_versions:
        releases.append({
            'version': match.group(1),
            'released': datetime.strptime(item.find('pubDate').text, "%a, %d %b %Y %H:%M:%S UT").strftime("%Y-%m-%d")
        })
