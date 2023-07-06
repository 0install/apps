from urllib.request import urlopen, Request
import re

data = urlopen(Request('https://www.scala-lang.org/files/archive/', headers={'User-Agent': 'Mozilla'})).read().decode('utf-8')
matches = re.findall(r'scala-([0-9\.\-M]+)\.zip<\/a>\s+<\/td><td align="right">(....-..-..)', data)
releases = [{
    'version': match[0].replace('M', 'pre'),
    'version-original': match[0],
    'stability': 'testing' if 'M' in match[0] else 'stable',
    'released': match[1]
} for match in matches]
