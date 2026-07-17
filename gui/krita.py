from urllib.request import urlopen, Request
import re

def regex(url, pattern):
    data = urlopen(Request(url, headers={'User-Agent': 'Mozilla'})).read().decode('utf-8')
    return re.findall(pattern, data)

def releases(filename_template):
    for version in regex('https://download.kde.org/stable/krita/', r'href="(\d[\d.]*)/">\1/</a>'):
        filename = filename_template.format(version)
        for released in regex(
                'https://download.kde.org/stable/krita/' + version + '/',
                r'>' + re.escape(filename) + r'</a>\s*</td><td align="right">(\d{4}-\d{2}-\d{2})'):
            yield {
                'version': version,
                'released': released
            }
            break
