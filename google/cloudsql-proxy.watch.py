from urllib import request
import json

excluded_versions = ['1.05', '1.06', '1.07', '1.08', '1.09', '1.10', '1.11', '1.12']

data = request.urlopen('https://api.github.com/repos/GoogleCloudPlatform/cloudsql-proxy/releases').read().decode('utf-8')
releases = [{'version': release['tag_name'], 'released': release['published_at'][0:10]} for release in json.loads(data) if release['tag_name'] not in excluded_versions]
