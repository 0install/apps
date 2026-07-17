import re
from urllib import request

BASE = 'https://archive.apache.org/dist/netbeans/netbeans/'
HEADERS = {'User-Agent': 'Mozilla/5.0'}

def fetch(url):
    return request.urlopen(request.Request(url, headers=HEADERS)).read().decode('utf-8')

index = fetch(BASE)
versions = [m for m in re.findall(r'<a href="([^"?/]+)/">', index) if re.fullmatch(r'\d+', m) and int(m) >= 13]

releases = []
for version in sorted(versions, key=int, reverse=True)[:8]:
    listing = fetch('%s%s/' % (BASE, version))
    m = re.search(r'netbeans-%s-bin\.zip</a>\s*(\d{4}-\d{2}-\d{2})' % re.escape(version), listing)
    if m:
        releases.append({
            'version': version,
            'released': m.group(1),
            'stability': 'stable',
        })
