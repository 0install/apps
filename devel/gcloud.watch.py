from urllib import request
import json


data = request.urlopen('https://www.googleapis.com/storage/v1/b/cloud-sdk-release/o?prefix=google-cloud-sdk-2').read().decode('utf-8')
releases = [{
    'version': release['name'].replace('google-cloud-sdk-', '').replace('-windows-x86_64.zip', ''),
    'released': release['timeCreated'][0:10]
} for release in json.loads(data)['items'] if str.endswith(release['name'], '-windows-x86_64.zip')]
