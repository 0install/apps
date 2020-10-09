from urllib import request
import json
import re

data = request.urlopen('https://api.github.com/repos/Microsoft/vscode/tags').read().decode('utf-8')
releases = [{'version': tag['name'].strip('v')} for tag in json.loads(data) if not '/' in tag['name'] and not 'GOOD' in tag['name'] and not 'BAD' in tag['name'] and not 'bad' in tag['name'] and not 'conflict' in tag['name'] and not 'vsda' in tag['name'] and tag['name'] != '1.999.0']
