from urllib import request
import json

data = request.urlopen('https://api.github.com/repos/0install/0install-dotnet/releases').read().decode('utf-8')
releases = [{'version': release['tag_name'], 'released': release['published_at'][0:10]} for release in json.loads(data) if any('0install-dotnet' in asset['name'] for asset in release['assets'])]
