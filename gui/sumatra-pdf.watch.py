import re
from urllib import request

data = request.urlopen('https://www.sumatrapdfreader.org/docs/Version-history.md').read().decode('utf-8')

releases = [{
    'version': m[0],
    'released': m[1],
} for m in re.findall(r'(?m)^#{1,2}\s*([\d]+\.[\d]+(?:\.[\d]+)?)\s*\(([\d]{4}-[\d]{2}-[\d]{2})\)', data)
   if int(m[1][0:4]) >= 2023]
