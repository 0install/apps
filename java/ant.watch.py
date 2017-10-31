from urllib import request
import re

data = request.urlopen('http://archive.apache.org/dist/ant/binaries/').read().decode('utf-8')
matches = re.findall(r'apache-ant-([0-9\.]+)-bin.tar.bz2<\/a>\s+(....-..-..)', data)
releases = [{'version': match[0], 'released': match[1]} for match in matches]
