#os=Linux
"""
     gnumpc 0watch script for packages from the mingw64 project

"""
from os.path import abspath, join, dirname
import sys
sys.path.insert(0, abspath(join(dirname(__file__), '..')))
from mingw64watch import get_new_version, \
                         get_mingw64_valid_new_package_item_map, \
                         get_mingw32_valid_new_package_item_map  # noqa: E402

NAME = 'mpc'
FEED = join(dirname(__file__), 'gnumpc.xml')

PKG_MAP_64 = get_mingw64_valid_new_package_item_map(NAME, FEED)
RELEASE64 = get_new_version(PKG_MAP_64)

PKG_MAP_32 = get_mingw32_valid_new_package_item_map(NAME, FEED)
RELEASE32 = get_new_version(PKG_MAP_32)

if RELEASE64 is None and RELEASE32 is None:
    exit()

if RELEASE64 is None or RELEASE32 is None:
    MSG = f"either the 32 or the 64 bit release is not ready for packaging"
    raise Exception(MSG)

if RELEASE64['version'] != RELEASE32['version']:
    raise Exception(f"""64bit version {RELEASE64['version']} does not match
                        32bit version {RELEASE32['version']}""")

if RELEASE64['license'] != RELEASE32['license']:
    raise Exception(f"""64bit license {RELEASE64['license']} does not match
                        32bit license {RELEASE32['license']}""")

if RELEASE64['packager'] != RELEASE32['packager']:
    raise Exception(f"""64bit packager {RELEASE64['packager']} does not match
                        32bit packager {RELEASE32['packager']}""")

if RELEASE64['desc'] != RELEASE32['desc']:
    raise Exception(f"""64bit description {RELEASE64['desc']} does not match
                        32bit description {RELEASE32['desc']}""")

RELEASE64['released32'] = RELEASE32['released']
RELEASE64['pkg_url32'] = RELEASE32['pkg_url']

releases = [RELEASE64]
# print(releases)
