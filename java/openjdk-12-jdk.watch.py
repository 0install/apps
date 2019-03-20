from urllib import request
import re

data = request.urlopen('http://jdk.java.net/12/').read().decode('utf-8')
releases = [{'version': re.findall(r'\/jdk12\/GPL\/openjdk-([0-9\.]+)_', data)[0]}]
