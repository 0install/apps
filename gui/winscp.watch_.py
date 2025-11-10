from urllib import request
import xml.etree.ElementTree as ET
import re
from datetime import datetime

data = request.urlopen('https://sourceforge.net/projects/winscp/rss?path=/WinSCP').read()

releases = []
for item in ET.fromstring(data).find('channel').findall('item'):
    match = re.search(r'([0-9\.]+)-Portable', item.find('title').text)
    if match and match.group(1).startswith('5') and 'beta' not in match.group(1) and 'RC' not in match.group(1):
        releases.append({
            'version': match.group(1),
            'released': datetime.strptime(item.find('pubDate').text, "%a, %d %b %Y %H:%M:%S UT").strftime("%Y-%m-%d")
        })
