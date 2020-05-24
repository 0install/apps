from urllib.request import Request, urlopen
import re
from datetime import datetime

data = urlopen(Request('https://ffmpeg.zeranoe.com/builds/win64/static/', headers={'User-Agent': 'Mozilla/5.0'})).read().decode('utf-8')
matches = re.findall(r'ffmpeg-([0-9\.]+)-win64-static\.zip<\/a>\s*(..-...-....)', data)
releases = [{'version': match[0], 'released': datetime.strftime(datetime.strptime(match[1], '%d-%b-%Y'), '%Y-%m-%d')} for match in matches]