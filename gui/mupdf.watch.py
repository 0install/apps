from urllib import request
import json
import re
import datetime

data = request.urlopen(request.Request('https://www.mupdf.com/downloads/index.html')).read().decode('utf-8')
						
matches =re.findall(r'>mupdf-([0-9\.]+)-windows.zip<', data)
data = request.urlopen(request.Request('https://www.mupdf.com/release_history.html')).read().decode('utf-8')
releases = []
for amatch in matches:
  date = datetime.datetime.today().date().isoformat()
  secondMatch = re.search(rf'MuPDF {amatch} \((....-..-..)\)',data)
  if secondMatch:
    date = secondMatch[1]

  releases.append({'version': amatch,'released': date })
    
releases
