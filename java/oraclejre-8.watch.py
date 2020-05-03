from urllib import request
import re
from datetime import datetime

data = request.urlopen('https://www.java.com/en/download/manual.jsp').read().decode('utf-8')
patch_level = re.findall(r'Recommended Version 8 Update (\d+)', data)[0]
released = re.findall(r'Release date (.+ \d+, \d\d\d\d)', data)[0]
bundle = re.findall(r'"Download Java software for Windows Offline" href="https://javadl.oracle.com/webapps/download/AutoDL\?BundleId=(\d+)_([0-9a-f]+)"', data)[0]
bundle_id_base = int(bundle[0])
bundle_suffix = bundle[1]

releases = [{
    'version': '8.0.' + patch_level,
    'released': datetime.strftime(datetime.strptime(released, '%B %d, %Y'), '%Y-%m-%d'),
    'patch-level': patch_level,
    'bundle-suffix': bundle_suffix,
    'bundle-id-linux-i586': str(bundle_id_base - 10),
    'bundle-id-linux-x64': str(bundle_id_base - 8),
    'bundle-id-windows-i586': str(bundle_id_base + 1),
    'bundle-id-windows-x64': str(bundle_id_base + 3)
}]
print(releases)
