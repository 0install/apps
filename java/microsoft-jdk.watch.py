from urllib import request
import re

data = request.urlopen('https://learn.microsoft.com/en-us/java/openjdk/download').read().decode('utf-8')

# The download filenames carry only the version; the build number (needed for the
# extracted directory name jdk-{version}+{buildnumber}) is only exposed via the
# source-code links, e.g. .../openjdk-jdk25u/tree/release/jdk-25.0.3_9
builds = dict(re.findall(r'openjdk-jdk[0-9]+u/tree/release/jdk-([0-9]+\.[0-9]+\.[0-9]+)_([0-9]+)', data))

versions = sorted(set(re.findall(r'microsoft-jdk-([0-9]+\.[0-9]+\.[0-9]+)-linux-x64\.tar\.gz', data)), key=lambda v: list(map(int, v.split('.'))))
releases = [{'version': v, 'buildnumber': builds[v]} for v in versions if v in builds]
