from urllib import request
import re
from datetime import datetime

def convert(match):
    return {
        'version': match[0].replace('alpha', 'pre1-').replace('beta', 'pre2-') + '-0', # -0 suffix to ensure SDK is always considered "newer" than regular build
        'version-original': match[0],
        'stability': 'developer' if ('alpha' in match[0] or 'beta' in match[0]) else ('testing' if 'rc' in match[0] else 'stable'),
        'released': datetime.strftime(datetime.strptime(match[1], '%d-%b-%Y'), '%Y-%m-%d')
    }

data = request.urlopen('https://dl.nwjs.io/').read().decode('utf-8')
matches = re.findall(r'v([0-9\.\-alphabetarc]+)\/<\/a><\/td><td align="right">(..-...-....)', data)
releases = [convert(match) for match in matches if match[0][0:3] == '0.2']
