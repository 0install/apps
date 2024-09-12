#os=Windows
from urllib import request
import re
from datetime import datetime

excluded_versions = ['24.8.1.2']

data = request.urlopen('https://downloadarchive.documentfoundation.org/libreoffice/old/').read().decode('utf-8')
matches = re.findall(r'>([0-9\.]+)\/<\/a><\/td><td align="right">(..-...-....)', data)
releases = [{
    'version': match[0].replace('.alpha', '-pre').replace('.beta', '-rc'),
    'version-original': match[0],
    'released': datetime.strftime(datetime.strptime(match[1], '%d-%b-%Y'), '%Y-%m-%d')
} for match in matches if not (match[0].startswith("3.") or match[0].startswith("4.") or match[0].startswith("5.") or match[0] in excluded_versions)]
