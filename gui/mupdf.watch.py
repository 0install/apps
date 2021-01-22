''' 0watch script for mupdf '''
import re
from urllib import request
from datetime import datetime

releases = []
REGEX = r'>mupdf-([0-9\.]+)-windows.zip<'
HOME = 'https://www.mupdf.com/downloads/index.html'
HIST = 'https://www.mupdf.com/release_history.html'
today = datetime.datetime.today().date().isoformat()

matches = re.findall(
    REGEX,
    request.urlopen(request.Request(HOME)).read().decode('utf-8')
)
release_history = request.urlopen(request.Request(HIST)).read().decode('utf-8')

for match in matches:
    date_regex = rf'MuPDF {match} \((....-..-..)\)'
    release_match = re.search(date_regex, release_history)
    releases.append({
        'version': match,
        'released': release_match[1] if release_match else today
    })
