from urllib import request
import re

def convert(match):
    return {
        'version': match[0].replace('M', 'pre'),
        'version-original': match[0],
        'stability': 'testing' if 'M' in match[0] else 'stable',
        'released': match[1]
    }

data = request.urlopen('http://www.scala-lang.org/files/archive/').read().decode('utf-8')
matches = re.findall(r'scala-([0-9\.\-M]+)\.zip<\/a>\s+<\/td><td align="right">(....-..-..)', data)
releases = [convert(match) for match in matches]
