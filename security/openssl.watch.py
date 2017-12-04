from urllib import request
import re

def convert(match):
    return {'version': match[0] + "-" + (str(ord(match[1][0]) - 96) if len(match[1]) == 1 else "0"),
        'version-original': match[0] + match[1],
        'released': match[2]
    }

data = request.urlopen('https://indy.fulgan.com/SSL/').read().decode('utf-8')
matches = re.findall(r'">openssl-([0-9]\.[0-9]\.[0-9])([a-z]?)-x64_86-win64.zip</a>\s+(....-..-..)', data)
releases = [convert(match) for match in matches]
