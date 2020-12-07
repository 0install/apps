from urllib import request
import re

data = request.urlopen('http://www.scala-lang.org/files/archive/').read().decode('utf-8')
matches = re.findall(r'scala-([0-9\.\-M]+)\.zip<\/a>\s+<\/td><td align="right">(....-..-..)', data)
releases = [{
    'version': match[0].replace('M', 'pre'),
    'version-original': match[0],
    'stability': 'testing' if 'M' in match[0] else 'stable',
    'released': match[1]
} for match in matches]
