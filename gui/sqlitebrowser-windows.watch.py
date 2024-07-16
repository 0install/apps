from urllib import request
import re

releases = []
skipped_releases = ['2024-06-15', '2024-06-16']

data = request.urlopen('https://nightlies.sqlitebrowser.org/win64/').read().decode('utf-8')
for month in re.findall(r'href="(\d{4}-\d{2})', data):
    if str.startswith(month, '2023'): continue
    data = request.urlopen('https://nightlies.sqlitebrowser.org/win64/' + month + '/').read().decode('utf-8')
    for released in re.findall(r'href="DB\.Browser\.for\.SQLite-(\d{4}-\d{2}-\d{2})-win64', data):
        if released in skipped_releases: continue        
        releases.append({
            'month': month,
            'released': released,
            'version': released.replace('-', '.')
        })
