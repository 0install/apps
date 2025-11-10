#os=Linux
from urllib import request
import xml.etree.ElementTree as ET
import re
from datetime import datetime

data = request.urlopen('https://sourceforge.net/projects/gptfdisk/rss?path=/gptfdisk').read()

releases = []
for item in ET.fromstring(data).find('channel').findall('item'):
    match = re.search(r'([0-9\.]+)\.zip', item.find('title').text)
    if match and match.group(1).startswith('1.0'):
        releases.append({
            'version': match.group(1),
            'released': datetime.strptime(item.find('pubDate').text, "%a, %d %b %Y %H:%M:%S UT").strftime("%Y-%m-%d")
        })
