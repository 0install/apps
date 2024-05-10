from urllib import request
import re

excluded_versions = ['0.45', '0.46', '0.47', '0.48', '0.49', '0.50', '0.51']

data = request.urlopen('https://www.chiark.greenend.org.uk/~sgtatham/putty/changes.html').read().decode('utf-8')
matches = re.findall(r'>([0-9.]+)<\/a>\n\(released (....-..-..)', data)
releases = [{'version': match[0], 'released': match[1]} for match in matches if not match[0] in excluded_versions]
