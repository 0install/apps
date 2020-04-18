#os=Windows
from urllib import request
import re

data = request.urlopen('http://strawberryperl.com/releases.html').read().decode('utf-8')
matches = re.findall(r'Strawberry Perl ([0-9\.]+) \((....-..-..)\)', data)
releases = [{'version': match[0], 'released': match[1]} for match in matches if int(match[1][0:4]) > 2011]
