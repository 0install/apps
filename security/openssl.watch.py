from urllib import request
import json

# Convert OpenSSL version number (e.g., 1.1.0b) into Zero Install version number (e.g., 1.1.0-2)
def convert(version):
    return version[0:5] + "-" + str(ord(version[5]) - 96) if len(version) == 6 else version

data = json.loads(request.urlopen('https://api.bintray.com/packages/vszakats/generic/openssl').read().decode('utf-8'))
releases = [{'version': convert(version), 'version-original': version, 'released': data['updated'][0:10]} for version in data['versions']]
