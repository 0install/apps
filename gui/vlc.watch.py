#os=Windows
from urllib import request
import re
from datetime import datetime

skipped_versions = ['3.0.11.1']

data = request.urlopen('https://get.videolan.org/vlc/').read().decode('utf-8')
matches = re.findall(r'/">([0-9\.]+)/</a>\s+(..-...-....)', data)
releases = [{'version': match[0], 'released': datetime.strftime(datetime.strptime(match[1], '%d-%b-%Y'), '%Y-%m-%d')} for match in matches if match[0].startswith('3.') and match[0] not in skipped_versions]
