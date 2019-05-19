from urllib import request
import re
from datetime import datetime

def convert(match):
    return {
        'version': match[0].replace('.alpha', '-pre').replace('.beta', '-rc'),
        'version-original': match[0],
        'released': datetime.strftime(datetime.strptime(match[1], '%d-%b-%Y'), '%Y-%m-%d')
    }

data = request.urlopen('https://downloadarchive.documentfoundation.org/libreoffice/old/').read().decode('utf-8')
matches = re.findall(r'/">([0-9\.]+)/</a></td><td align="right">(..-...-....)', data)
releases = [convert(match) for match in matches if match[0].startswith("6")]
