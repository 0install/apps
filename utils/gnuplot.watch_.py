from urllib import request
import xml.etree.ElementTree as ET
import re
from datetime import datetime

excluded_versions = ['5.0.2', '5.2.1', '5.4.9', '5.4.10']

data = request.urlopen('https://sourceforge.net/projects/gnuplot/rss?path=/gnuplot').read()

releases = []
for item in ET.fromstring(data).find('channel').findall('item'):
    match = re.search(r'([0-9\.]+)-win64', item.find('title').text)
    if match and match.group(1).startswith('5.') and match.group(1) not in excluded_versions:
        releases.append({
            'version': match.group(1),
            'version-without-dots': match.group(1).replace('.', ''),
            'released': datetime.strptime(item.find('pubDate').text, "%a, %d %b %Y %H:%M:%S UT").strftime("%Y-%m-%d")
        })
