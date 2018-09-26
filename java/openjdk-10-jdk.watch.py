from urllib import request
import re

data = request.urlopen('http://jdk.java.net/10/').read().decode('utf-8')
match = re.findall(r'\/jdk10\/([0-9\.]+)\/([0-9a-f]+)\/([0-9]+)\/openjdk-', data)[0]
releases = [{'version': match[0], 'build-id': match[1], 'build-counter': match[2]}]
