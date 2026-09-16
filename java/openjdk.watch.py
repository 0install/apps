from urllib import request
import re

index = request.urlopen('https://jdk.java.net/').read().decode('utf-8')
major = re.search(r'GA Releases.*?<a href="\./(\d+)/">JDK \1</a>', index, re.DOTALL).group(1)

data = request.urlopen(f'https://jdk.java.net/{major}/').read().decode('utf-8')
matches = re.findall(r'GA\/jdk([0-9\.]+)\/([0-9a-f]+\/[0-9]+)\/', data)[0]
releases = [{'version': matches[0], 'release-id': matches[1]}]
