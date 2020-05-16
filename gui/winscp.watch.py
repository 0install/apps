from urllib import request
import re

data = request.urlopen('https://sourceforge.net/projects/winscp/files/WinSCP/').read().decode('utf-8')
matches = re.findall(r'([0-9\.]+)</span></a>\n\s*</th>\n\s*<td headers="files_date_h" class="opt"><abbr title="(....-..-..)', data)
releases = [{'version': match[0], 'released': match[1]} for match in matches if match[0][0] == '5' and not 'beta' in match[0] and not 'RC' in match[0]]
