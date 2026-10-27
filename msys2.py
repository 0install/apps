# Helpers for listing packages in the MinGW repositories of MSYS2.

from urllib import request, parse
import re
from datetime import datetime

prefixes = {
    'ucrt64': 'mingw-w64-ucrt-x86_64',
    'clangarm64': 'mingw-w64-clang-aarch64',
}

def packages(repo, name):
    """Returns {(pkgver, pkgrel): released} for all builds of a package in a repository."""
    # Unquote to match names like libc++, which the listing links as libc%2B%2B
    data = parse.unquote(request.urlopen('https://repo.msys2.org/mingw/' + repo + '/').read().decode('utf-8'))
    return {(match[0], match[1]): datetime.strptime(match[2], '%d-%b-%Y').strftime('%Y-%m-%d')
            for match in re.findall(r'href="' + re.escape(prefixes[repo] + '-' + name) + r'-(\d[^-"]*)-(\d+)-any\.pkg\.tar\.zst">[^<]*</a>\s+(\d\d-\w\w\w-\d\d\d\d)', data)}

def version(pkgver):
    """Converts a pacman pkgver to a 0install version, or returns None if it can't."""
    # Epochs, e.g. 1~3.0.10
    result = re.sub(r'^\d+~', '', pkgver)
    # Git snapshots, e.g. 14.0.0.r569.g34eeafb7d
    result = re.sub(r'\.r(\d+)\.g[0-9a-f]+$', r'-post\1', result)
    return result if re.fullmatch(r'\d+(\.\d+)*(-(pre|rc|post)\d+)?', result) else None

def releases(name, repos=('ucrt64', 'clangarm64')):
    """Returns the newest build of each version of a package that is available in all repositories.
    Provides the keys version, pkgver (as used in the archive filename), pkgrel and released."""
    builds = [packages(repo, name) for repo in repos]

    latest = {}
    for (pkgver, pkgrel), date in builds[0].items():
        if all((pkgver, pkgrel) in other for other in builds[1:]) and int(pkgrel) > int(latest.get(pkgver, ('0', ''))[0]):
            latest[pkgver] = (pkgrel, date)

    return [{
        'version': version(pkgver),
        'pkgver': pkgver,
        'pkgrel': pkgrel,
        'released': date
    } for pkgver, (pkgrel, date) in latest.items() if version(pkgver)]
