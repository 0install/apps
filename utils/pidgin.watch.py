from urllib import request
import re

excluded_versions = ['1.5.1', '2.0.0', '2.0.1', '2.0.2', '2.1.0', '2.1.1', '2.2.0', '2.2.1', '2.2.0', '2.5.9', '2.6.0', '2.13.0']

data = request.urlopen('https://sourceforge.net/projects/pidgin/files/Pidgin/').read().decode('utf-8')
matches = re.findall(r'([0-9\.]+)</span></a>\n\s*</th>\n\s*<td headers="files_date_h" class="opt"><abbr title="(....-..-..)', data)
releases = [{'version': match[0], 'released': match[1]} for match in matches if not match[0] in excluded_versions]
