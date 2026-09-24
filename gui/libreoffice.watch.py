#os=Windows
from urllib import request
from urllib.error import HTTPError
import os, re
from datetime import datetime

base_url = 'https://downloadarchive.documentfoundation.org/libreoffice/old/'
excluded_versions = ['24.8.1.2', '26.2.0.2']

with open(os.path.join(os.path.dirname(__file__), 'libreoffice.xml'), 'r', encoding='utf-8') as file:
    existing_feed = file.read()

def has_msi(version):
    if f'/old/{version}/' in existing_feed:
        return True
    try:
        listing = request.urlopen(f'{base_url}{version}/win/x86_64/').read().decode('utf-8')
    except HTTPError:
        return False
    return f'href="LibreOffice_{version}_Win_x86-64.msi"' in listing

data = request.urlopen(base_url).read().decode('utf-8')
matches = re.findall(r'>([0-9\.]+)\/<\/a><\/td><td align="right">(..-...-....)', data)
releases = [{
    'version': match[0].replace('.alpha', '-pre').replace('.beta', '-rc'),
    'version-original': match[0],
    'released': datetime.strftime(datetime.strptime(match[1], '%d-%b-%Y'), '%Y-%m-%d')
} for match in matches if not (match[0].startswith(("3.", "4.", "5.")) or match[0] in excluded_versions) and has_msi(match[0])]
