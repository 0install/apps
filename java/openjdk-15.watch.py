from urllib import request
import re

data = request.urlopen('http://jdk.java.net/15/').read().decode('utf-8')
matches = re.findall(r'GA\/jdk([0-9\.]+)\/([0-9a-f]+\/[0-9]+)\/', data)[0]
releases = [{'version': matches[0], 'release-id': matches[1]}]
