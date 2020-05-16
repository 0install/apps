from urllib import request
import re
from datetime import datetime

data = request.urlopen('https://curl.haxx.se/changes.html').read().decode('utf-8')
matches = re.findall(r'<h2> Fixed in (\d+\.\d+\.\d+) - (\w+ \d+ \d+) <\/h2>', data)
releases = [{
    'version': match[0],
    'released': datetime.strftime(datetime.strptime(match[1], '%B %d %Y'), '%Y-%m-%d')
} for match in matches if int(match[1][-4:]) >= 2020]
