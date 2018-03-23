from urllib import request
import re

data = request.urlopen('https://sourceforge.net/projects/pidgin/files/GTK%2B%20for%20Windows/').read().decode('utf-8')
matches = re.findall(r'([0-9\.]+)</span></a></th>\n\s*<td headers="files_date_h" class="opt"><abbr title="(....-..-..)', data)
releases = [{'version': match[0], 'released': match[1]} for match in matches]