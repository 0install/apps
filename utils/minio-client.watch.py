from urllib.request import urlopen, Request
import re

data = urlopen(Request('https://dl.min.io/client/mc/release/darwin-arm64/archive/')).read().decode('utf-8')
matches = re.findall(r'mc\.RELEASE\.((\d\d\d\d-\d\d-\d\d)T\d\d-\d\d-\d\dZ)<', data)
releases = [{
    'version': match[1].replace('-', '.'),
    'released': match[1],
    'timestamp': match[0]
} for match in matches]
