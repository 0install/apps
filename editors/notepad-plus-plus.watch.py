from urllib import request
import xml.etree.ElementTree as ET
from datetime import datetime

def parse(data):
    for item in ET.fromstring(data).find('channel').findall('item'):
        title = item.find('title').text
        pubDate = datetime.strptime(item.find('pubDate').text[5:16], '%d %b %Y')
        if title.startswith('Notepad++ ') and title.endswith(' released'):
            yield {'version': title[10:-9], 'released': datetime.strftime(pubDate, '%Y-%m-%d')}

data = request.urlopen('https://notepad-plus-plus.org/feed.rss').read().decode('utf-8')
releases = list(parse(data))
