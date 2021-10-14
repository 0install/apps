from urllib import request
import re

data = request.urlopen('https://raw.githubusercontent.com/yaml/pyyaml/master/CHANGES').read().decode('utf-8')
matches = re.findall(r'([0-9\.]+) \((....-..-..)\)', data)
releases = [{'version': re.sub(r"\.0(\d)", r".\1", match[0]), 'version-original': match[0], 'released': match[1]} for match in matches]
