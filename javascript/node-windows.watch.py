#os=Windows
from urllib import request
import re
from datetime import datetime

excluded_versions = ['9.11.0']

data = request.urlopen('https://nodejs.org/en/download/releases/').read().decode('utf-8')
matches = re.findall(r'<td data-label="Version">Node.js ([0-9\.]+)<\/td>\n\s*<td data-label="LTS">([A-Za-z]*)<\/td>\n\s*<td data-label="Date"><time>(....-..-..)<\/time><\/td>', data)
releases = [{
    'version': match[0],
    'stability': 'testing' if match[1] == '' else 'stable',
    'released': match[2]
} for match in matches if match[0][0] != '0' and not match[0] in excluded_versions]
