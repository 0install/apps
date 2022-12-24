from urllib import request
import re

data = request.urlopen('http://wiki.overbyte.eu/wiki/index.php/ICS_Download').read().decode('utf-8')
matches = re.findall(r'<td>(....-..-..)<\/td>\n<td><a rel="nofollow" class="external text" href="http:\/\/wiki\.overbyte\.eu\/arch\/openssl-([0-9\.]+[a-z]?)-win64\.zip', data)
releases = [{
    # Convert OpenSSL version number (e.g., 1.1.0b) into Zero Install version number (e.g., 1.1.0-2)
    'version': match[1][0:5] + "-" + str(ord(match[1][5]) - 96) if len(match[1]) == 6 else match[1],
    'version-original': match[1],
    'released': match[0]
} for match in matches]
