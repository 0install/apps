from urllib import request
import re

data = request.urlopen('http://jdk.java.net/11/').read().decode('utf-8')
match = re.findall(r'openjdk-([0-9\.]+)\+([0-9]+)_', data)[0]
releases = [{'version': match[0], 'build-counter': match[1]}]
