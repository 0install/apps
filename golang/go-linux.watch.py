#os=Linux
from urllib import request
import re

excluded_versions = ['1', '1.0.1', '1.0.2', '1.0.3', '1.1', '1.1.1', '1.1.2', '1.2', '1.2.1']

data = request.urlopen('https://golang.org/doc/devel/release.html').read().decode('utf-8')
matches = re.findall(r'go([0-9\.]+) \(released (..../../..)\)', data)
releases = [{'version': match[0], 'released': match[1].replace('/', '-')} for match in matches if match[0] not in excluded_versions]
