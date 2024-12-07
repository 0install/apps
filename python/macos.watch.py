#os=manual-Darwin
from urllib import request
import gzip, re
from datetime import datetime
import os, subprocess, shutil, tempfile

def scrape_website():
    bytes = request.urlopen('https://www.python.org/downloads/macos/').read()

    # Response is sometimes, but not always, GZip-compressed
    try: bytes = gzip.decompress(bytes)
    except: pass

    return bytes.decode('utf-8')

def get_peer(file_name):
    return os.path.join(os.path.dirname(__file__), file_name)

def read_feed():
    with open(get_peer('macos.xml'), 'r') as file:
        return file.read()

def extract_installer(version_patch, version_full, version):
    dest_dir = f"macos-{version}"
    with tempfile.NamedTemporaryFile(prefix="python-", suffix=".pkg") as pkg_file:
        subprocess.run(["curl", "-sSfL", f"https://www.python.org/ftp/python/{version_patch}/python-{version_full}-macos11.pkg", "-o", pkg_file.name], check=True)
        with tempfile.TemporaryDirectory(prefix="python-") as extract_dir:
            subprocess.run(["pkgutil", "--expand-full", pkg_file.name, os.path.join(extract_dir, "full")], check=True)
            os.makedirs(dest_dir)
            shutil.move(os.path.join(extract_dir, "full", "Python_Framework.pkg", "Payload"), os.path.join(dest_dir, "Python.framework"))

data = scrape_website()
existing_feed = read_feed()

releases = []
for match in re.findall(r'Python (3)\.([0-9]+)\.([0-9]+)([0-9abrc]*?) - (.*)<\/a>', data):
    version_suffix = match[3]
    version_minor = match[0] + "." + match[1]
    version_patch = version_minor + "." + match[2]
    version_full = version_patch + version_suffix

    if not (version_full + "-macos11.pkg") in data:
        continue

    if version_suffix.startswith('rc'):
        stability = 'testing'
        version = version_patch + "-" + version_suffix
    #elif version_suffix.startswith('b'):
    #    stability = 'developer'
    #    version = version_patch + "-" + version_suffix.replace("b", "pre")
    #elif version_suffix.startswith('a'):
    #    stability = 'developer'
    #    version = version_patch + "-" + version_suffix.replace("a", "pre-pre")
    elif version_suffix != "":
        continue
    else:
        stability = 'stable'
        version = version_patch

    try:
        released_parsed = datetime.strptime(match[4].replace('Sept.', 'Sep.'), '%b. %d, %Y')
    except ValueError:
        released_parsed = datetime.strptime(match[4], '%B %d, %Y')
    released = datetime.strftime(released_parsed, '%Y-%m-%d')

    if not os.path.exists(get_peer(f'macos-{version}.xml')) and not f'"{version_full}"' in existing_feed:
        extract_installer(version_patch, version_full, version)

    releases.append({
        'version': version,
        'version-minor': version_minor,
        'stability': stability,
        'released': released
    })
