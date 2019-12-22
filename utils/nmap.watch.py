from urllib import request
import re

data = request.urlopen('http://nmap.org/dist/').read().decode('utf-8')
matches = re.findall(r'nmap-([0-9\.]+)-win32.zip</a></td><td align="right">(....-..-..)', data)
releases = [{'version': match[0], 'released': match[1]} for match in matches if not match[0].startswith('2.0')]
