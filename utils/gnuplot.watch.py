from urllib import request
import re

excluded_versions = ['5.0.2', '5.2.1', '5.4.1', '5.4.2']

data = request.urlopen('https://sourceforge.net/projects/gnuplot/files/gnuplot/').read().decode('utf-8')
matches = re.findall(r'([0-9\.]+)</span></a>\n\s*</th>\n\s*<td headers="files_date_h" class="opt"><abbr title="(....-..-..)', data)
releases = [{'version': match[0], 'version-without-dots': match[0].replace('.', ''), 'released': match[1]} for match in matches if match[0].startswith('5.') and not match[0] in excluded_versions]
