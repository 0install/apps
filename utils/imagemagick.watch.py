from urllib import request
import json
import re

data = request.urlopen(request.Request('https://imagemagick.org/download/binaries/')).read().decode('utf-8')
						
matches =re.findall(r'ImageMagick-([-0-9\.]+)-portable-Q16-x86.zip">ImageMagick-[-0-9\.]+\.\.&gt;</a></td><td align="right">(....-..-..)', data)
releases = [{'version': match[0], 'released': match[1]} for match in matches]
