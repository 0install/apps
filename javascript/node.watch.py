from urllib import request
import re
from datetime import datetime

def convert(match):
    return {
        'version': match[0],
        'stability': 'testing' if match[1] == '' else 'stable',
        'released': match[2]
    }

data = request.urlopen('https://nodejs.org/en/download/releases/').read().decode('utf-8')
matches = re.findall(r'<td data-label="Version">Node.js v([0-9\.]+)<\/td>\n\s*<td data-label="LTS">([A-Za-z]*)<\/td>\n\s*<td data-label="Date"><time>(....-..-..)<\/time><\/td>', data)
releases = [convert(match) for match in matches if match[0][0] != '0']
