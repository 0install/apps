#os=Windows
from urllib import request
import json

data = request.urlopen('https://api.github.com/repos/hashicorp/vagrant/tags').read().decode('utf-8')
releases = [{'version': tag['name'].strip('v')} for tag in json.loads(data) if not str.startswith(tag['name'], 'v0.') and not str.startswith(tag['name'], 'v1.')]
