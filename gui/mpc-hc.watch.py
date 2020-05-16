from urllib import request
import json

excluded_versions = ['1.7.8', '1.7.12']

data = request.urlopen('https://api.github.com/repos/mpc-hc/mpc-hc/tags').read().decode('utf-8')
releases = [{'version': tag['name']} for tag in json.loads(data) if not '_' in tag['name'] and not tag['name'] in excluded_versions]
