#os=Windows
from urllib import request
import json

data = request.urlopen('https://api.github.com/repos/Azure/azure-cli/releases').read().decode('utf-8')
releases = [{
    'version': release['tag_name'][len('azure-cli-'):],
    'released': release['published_at'][0:10]
} for release in json.loads(data) if not release['prerelease'] and int(release['published_at'][0:4]) >= 2020]
