from urllib import request
import re

excluded_versions = ['7.52.0', '7.54.1', '7.55.0', '7.56.1']

data = request.urlopen('https://dl.uxnr.de/build/curl/curl_winssl_msys2_mingw64_stc/').read().decode('utf-8')
matches = re.findall(r'curl-([0-9\.]+)\/<\/a><\/td><td align="right">(....-..-..)', data)
releases = [{'version': match[0], 'released': match[1]} for match in matches if not match[0] in excluded_versions]
