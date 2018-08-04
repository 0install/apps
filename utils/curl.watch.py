from urllib import request
import json

data = json.loads(request.urlopen('https://api.bintray.com/packages/vszakats/generic/curl').read().decode('utf-8'))
releases = [{'version': version, 'released': data['updated'][0:10]} for version in data['versions']]
