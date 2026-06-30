from urllib import request
import re

data = request.urlopen('https://learn.microsoft.com/en-us/java/openjdk/download').read().decode('utf-8')
matches = re.findall(r'microsoft-jdk-([0-9]+\.[0-9]+\.[0-9]+)-linux-x64\.tar\.gz', data)
versions = sorted(set(matches), key=lambda v: list(map(int, v.split('.'))))
releases = [{'version': v} for v in versions]
