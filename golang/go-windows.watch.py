#os=Windows
from urllib import request
import re

data = request.urlopen('https://golang.org/doc/devel/release.html').read().decode('utf-8')
matches = re.findall(r'go([0-9\.]+)\n\s+\(released (....-..-..)\)', data)
releases = [{'version': match[0], 'released': match[1]} for match in matches if match[0] ]
