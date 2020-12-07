from urllib import request
import re

data = request.urlopen('http://archive.apache.org/dist/maven/maven-3/').read().decode('utf-8')
matches = re.findall(r'([0-9\.\-alphabeta]+)\/<\/a>\s+(....-..-..)', data)
releases = [{
    'version': match[0].replace('alpha', 'pre1').replace('beta', 'pre2'),
    'version-original': match[0],
    'stability': 'developer' if 'alpha' in match[0] else ('testing' if 'beta' in match[0] else 'stable'),
    'released': match[1]
} for match in matches]
