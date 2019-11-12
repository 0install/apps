from urllib import request
import json
import re

def handle(version):
    linux64url = request.urlopen('https://vscode-update.azurewebsites.net/' + version + '/linux-x64/stable').url
    return {
        'version': version,
        'release-id': re.search('stable/([0-9a-f]{40})/code', linux64url).group(1),
        'linux-amd64-timestamp': re.search('-([0-9]{10})', linux64url).group(1)
    }

data = request.urlopen('https://api.github.com/repos/Microsoft/vscode/tags').read().decode('utf-8')
releases = [handle(tag['name'].strip('v')) for tag in json.loads(data) if not '/' in tag['name'] and not 'GOOD' in tag['name'] and not 'BAD' in tag['name'] and not 'bad' in tag['name'] and not 'conflict' in tag['name'] and not 'vsda' in tag['name'] and tag['name'] != '1.999.0']
