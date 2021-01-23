import re
from urllib import request
from datetime import datetime

downloads = request.urlopen(request.Request('https://www.mupdf.com/downloads/index.html')).read().decode('utf-8')
matches = re.findall(r'>mupdf-([0-9\.]+)-windows.zip<', downloads)

release_history = request.urlopen(request.Request('https://www.mupdf.com/release_history.html')).read().decode('utf-8')
today = datetime.today().date().isoformat()

releases = []
for match in matches:
    release_match = re.search(rf'MuPDF {match} \((....-..-..)\)', release_history)
    releases.append({
        'version': match,
        'released': release_match[1] if release_match else today
    })
