from urllib import request
import json

data = request.urlopen('https://api.github.com/repos/hashicorp/packer/tags').read().decode('utf-8')
releases = [{'version': tag['name'].strip('v')} for tag in json.loads(data) if not '-' in tag['name']]
