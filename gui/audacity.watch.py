from urllib import request
import re

data = request.urlopen('https://fossies.org/windows/misc/').read().decode('utf-8')
matches = re.search(r'>audacity-win-([0-9.]+)-64bit\.zip', data)
releases = [{'version': matches[1]}]
