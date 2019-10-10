from urllib import request
import json
import re

data = request.urlopen(request.Request('https://eternallybored.org/misc/wget/releases')).read().decode('utf-8')
matches =re.findall(r'">wget-([0-9\.]+)-win64\.zip</a>\s+(....-..-..)', data)
releases = [{'version': match[0], 'released': match[1]} for match in matches]
