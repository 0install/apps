from urllib import request
import json
import re
from datetime import datetime

data = request.urlopen(request.Request('http://ftp.icm.edu.pl/packages/ImageMagick/binaries/')).read().decode('utf-8')
						
matches = re.findall(r'ImageMagick-(7\.[-0-9\.]+)-portable-Q16-x86.zip<\/a><\/td><td align="right">(..-...-....)', data)
releases = [{'version': match[0], 'released': datetime.strftime(datetime.strptime(match[1], '%d-%b-%Y'), '%Y-%m-%d')} for match in matches]
