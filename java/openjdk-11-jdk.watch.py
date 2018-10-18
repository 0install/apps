from urllib import request
import re

data = request.urlopen('http://jdk.java.net/11/').read().decode('utf-8')
match = re.findall(r'\/jdk11\/([0-9\.]+)\/GPL\/openjdk-([0-9\.]+)_', data)[0]
releases = [{'version': match[1], 'build-counter': match[0]}]
