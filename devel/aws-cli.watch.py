#os=Windows
from urllib import request
import json

data = request.urlopen('https://api.github.com/repos/aws/aws-cli/tags').read().decode('utf-8')
releases = [{
    'version': release['name']
} for release in json.loads(data) if release['name'][0:2] == '2.' and release['name'] != '2.0.32' and not 'dev' in release['name']]
