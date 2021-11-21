#os=Linux
from urllib import request
import re
from datetime import datetime

data = request.urlopen('https://dl.nwjs.io/').read().decode('utf-8')
matches = re.findall(r'v([0-9\.\-alphabetarc]+)\/<\/a><\/td><td align="right">(..-...-....)', data)
releases = [{
    'version': match[0].replace('alpha', 'pre1-').replace('beta', 'pre2-'),
    'version-original': match[0],
    'stability': 'developer' if ('alpha' in match[0] or 'beta' in match[0]) else ('testing' if 'rc' in match[0] else 'stable'),
    'released': datetime.strftime(datetime.strptime(match[1], '%d-%b-%Y'), '%Y-%m-%d')
} for match in matches if int(match[1][-4:]) >= 2020]
