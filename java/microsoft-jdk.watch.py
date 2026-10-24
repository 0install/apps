from urllib import request
import re

data = request.urlopen('https://learn.microsoft.com/en-us/java/openjdk/download').read().decode('utf-8')

# The download filenames carry only the version; the build number (needed for the
# extracted directory name jdk-{version}+{buildnumber}) is only exposed via the
# source-code links, e.g. .../openjdk-jdk25u/tree/release/jdk-25.0.3_9
builds = dict(re.findall(r'openjdk-jdk[0-9]+u/tree/release/jdk-([0-9]+(?:\.[0-9]+)+)_([0-9]+)', data))

# Some releases (e.g. hotfixes) are only published for some platforms,
# so only pick versions that have every archive the template references
archives = set(re.findall(r'microsoft-jdk-([0-9]+(?:\.[0-9]+)+)-((?:windows|linux|macos)-(?:x64|aarch64)\.(?:zip|tar\.gz))', data))
platforms = ['windows-x64.zip', 'windows-aarch64.zip', 'linux-x64.tar.gz', 'linux-aarch64.tar.gz', 'macos-x64.tar.gz', 'macos-aarch64.tar.gz']
versions = sorted({v for v, _ in archives if all((v, p) in archives for p in platforms)}, key=lambda v: list(map(int, v.split('.'))))
releases = [{'version': v, 'buildnumber': builds[v]} for v in versions if v in builds]
