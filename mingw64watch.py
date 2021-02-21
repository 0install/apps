""" functions to get package info and the archive from mingw64

    get_package_info gets the info for the package from the db
    validate_package check the packages crc and gpg signature
    fix_version normalize the version number of the package to 0install
    get_valid_new_package_item_map map of data for the new valid package
"""

import urllib
from urllib.request import urlopen
import io
from os import path
import tarfile
from datetime import datetime
import hashlib
import base64
import re
import gnupg


def get_valid_db(db_url, dst_file):
    """download the latest db signature
    validate the existing db file
    if it fails or doesnt exist download the db file and validate
    """
    sig = io.BytesIO(urlopen(urllib.request.Request(f'{db_url}.sig')).read())
    gpg = gnupg.GPG()

    with open(path.join(path.dirname(__file__), 'msys2.gpg')) as key_file:
        pkg_key = key_file.read()
        gpg.import_keys(pkg_key)

    result = gpg.verify_file(sig, data_filename=dst_file, close_file=False)
    if result.trust_level is None or result.trust_level <= result.TRUST_NEVER:
        print('downloading new db file')
        with urlopen(db_url) as in_file, open(dst_file, 'wb') as out_file:
            out_file.write(in_file.read())
        sig.seek(0)
        result = gpg.verify_file(sig, data_filename=dst_file)

    if result.trust_level is None or result.status != 'signature valid':
        print(f'''database {db_url} invalid signature
                {result.trust_level}, {result.status}''')
        exit(1)


def get_package_info(dbfilename, base_url, dst_folder, pkg_name):
    """ get the package info from the database file
        downloading it if necesary
    """
    dst_file = f'{dst_folder}/{dbfilename}'

    get_valid_db(f'{base_url}{dbfilename}', dst_file)

    tar = tarfile.open(dst_file)
    member = tar.next()
    while member is not None:

        if member.name.startswith(pkg_name):
            member = tar.next()
            break
        member = tar.next()

    if member is None:
        raise Exception(f"{pkg_name} not found in Packages file '{dst_file}'.")

    descfile = tar.extractfile(member)
    if descfile is not None:
        pkg_info = descfile.read().decode('utf-8')

    package_item_map = {}
    items = pkg_info.split('\n\n%')
    for item in items:
        key_value = item.split('%\n')
        if key_value[0] in package_item_map:
            existing = package_item_map[key_value[0]]
        else:
            existing = list()
        for line in key_value[1].splitlines():
            existing.append(line)
        package_item_map[key_value[0]] = existing

        # if item.startswith('%'):
        #    print(existing)

    if "%FILENAME" not in package_item_map:
        raise Exception('Filename not found in package data:\n' + pkg_info)
    return package_item_map


def save_file(url, file_path):
    """ download the file @ url to the local path
    """
    with urlopen(url) as in_file, open(file_path, 'wb') as out_file:
        out_file.write(in_file.read())


def validate_package(url, file_path, md5, sha256, pgp):
    """ download the file @ url to the local path
    and check it against hashes and pgp key
    """
    save_file(url, file_path)

    validated = False

    if md5 is not None:
        hash_md5 = hashlib.md5()
        hash_md5.update(open(file_path, 'rb').read())
        actual = hash_md5.hexdigest()
        if md5 != actual:
            msg = f"bad md5 for package! Was {actual}, but expected {md5}"
            raise Exception(msg)
        print(f'{file_path} has valid md5')
        validated = True

    if sha256 is not None:
        hash_sha256 = hashlib.sha256()
        hash_sha256.update(open(file_path, 'rb').read())
        actual = hash_sha256.hexdigest()
        if sha256 != actual:
            msg = f"bad sha256 for file! Was {actual}, but expected {sha256}"
            raise Exception(msg)
        print(f'{file_path} has valid sha256')
        validated = True

    if pgp is not None:
        sig = io.BytesIO(base64.b64decode(pgp))
        gpg = gnupg.GPG()
        result = gpg.verify_file(sig, data_filename=file_path, close_file=True)
        trust_level = result.trust_level
        if trust_level is None or result.status != 'signature valid':
            raise Exception(f"Invalid pgp signature for file!")
        print(f'{file_path} has valid pgp signature')
        validated = True

    return validated


def fix_version(version):
    """
        fix the passed version to conform with the format supported by 0install

        Version:= DottedList ("-" Modifier? DottedList?)*
        DottedList:= (Integer ("." Integer)*)
        Modifier:= "pre" | "rc" | "post"
    """
    numlist = r'(\d{1,10}([.]\d{1,10})*)'
    versionpattern = numlist + '(-(pre|rc|post)?' + numlist + '?)*'
    versionregex = re.compile(versionpattern)
    if versionregex.fullmatch(version):
        return version

    original_version = version

    if re.search(r'(\d|[.])rc\d', version):
        version = re.sub(r'(\d|[.])rc(\d)', r'\1-rc\2', version)

    hggit = re.search(r'r(\d{2, 5})[+]?[.]([0-9A-Fa-f]{7,12})[+]?-', version)
    if hggit:
        match = hggit.expand(r'\2')
        find_string = r'r(\d{2, 5})[+]?[.]' + match + r'[+]?-'
        value = int(match, 16)
        replacement = f'{value}'
        if value > 2147483648:
            replacement = ""
            sub_matches = [match[i:i + 3] for i in range(0, len(match), 3)]
            sub_replacements = [f'{int(x,16)}' for x in sub_matches]
            replacement = '.'.join(sub_replacements)
        version = re.sub(find_string, r'\1.' + replacement + '-', version)

    if re.search(r'[.]r\d', version):
        version = re.sub(r'[.]r(\d)', r'.\1', version)

    hexstringmatch = re.search(r'[0-9]*[A-Fa-f][0-9A-Fa-f]+', version)
    if hexstringmatch:
        match = hexstringmatch.group(0)
        value = int(match, 16)
        replacement = f'{value}'
        if value > 2147483648:
            replacement = ""
            sub_matches = [match[i:i + 3] for i in range(0, len(match), 3)]
            sub_replacements = [f'{int(x,16)}' for x in sub_matches]
            replacement = '.'.join(sub_replacements)
        version = re.sub(match, replacement, version)

    if versionregex.fullmatch(version):
        return version
    msg = f"{original_version} normalized to {version} but its still invalid"
    raise Exception(msg)


def timestamp_to_date_string(timestamp):
    """ convert a timestamp to a date string """
    return datetime.fromtimestamp(int(timestamp)).strftime('%Y-%m-%d')


def get_valid_new_pkg_item_map(base_url, dbfile, pkg_name_prefix, arch, feed):
    """ get the map of the first package that starts with the pkg_name_prefix
    located in the dbfilename at the base_url
    download the database file if necesary
    if the file for that version is not in the feed file then
        download it,
        check it against the hashes and pgp signature
        return the map of properties of that release
    aborts if the file is not used in the feed but the version is
    """

    dbfilename = f'{dbfile}.db.tar.gz'
    item_map = get_package_info(dbfilename, base_url, '/tmp', pkg_name_prefix)
    filename = item_map['%FILENAME'][0]

    version = item_map['VERSION'][0]
    version = fix_version(version)

    item_map['fixedversion'] = version
    item_map['arch'] = arch
    item_map['extract'] = dbfilename

    with open(feed) as feedfile:
        feedcontent = feedfile.read()
        if filename in feedcontent:
            return None

        if f'version="{version}"' in feedcontent:
            raise Exception(f"version {version} exists, not using {filename}")

    item_map['pkg_url'] = base_url + filename
    item_map['date'] = timestamp_to_date_string(item_map['BUILDDATE'][0])

    md5 = item_map['MD5SUM'][0]
    sha256 = item_map['SHA256SUM'][0]
    pgp = item_map['PGPSIG'][0]
    valid = validate_package(item_map['pkg_url'], filename, md5, sha256, pgp)
    if not valid:
        return None
    return item_map


def get_mingw64_valid_new_package_item_map(name, package):
    """ get_valid_new_pkg_item_map for mingw64 packages """
    url = 'http://repo.msys2.org/mingw/x86_64/'
    dbfile = 'mingw64'
    prefix = f'mingw-w64-x86_64-{name}-'
    x86_64 = 'x86_64'
    return get_valid_new_pkg_item_map(url, dbfile, prefix, x86_64, package)


def get_mingw32_valid_new_package_item_map(name, package):
    """ get_valid_new_pkg_item_map for mingw32 packages """
    url = 'http://repo.msys2.org/mingw/i686/'
    dbfile = 'mingw32'
    prefix = f'mingw-w64-i686-{name}-'
    i686 = 'i686'
    return get_valid_new_pkg_item_map(url, dbfile, prefix, i686, package)


def get_new_version(pkg_item_map):
    """
      takes a map of items
      return a release suitable for puting in the releases array
      aborts if the file is not used in the feed but the version is
    """
    if pkg_item_map is None:
        return pkg_item_map
    result = {'version': pkg_item_map['fixedversion'],
              'released':  pkg_item_map['date'],
              'name':   ''.join(pkg_item_map['BASE']).strip(),
              'desc':   ''.join(pkg_item_map['DESC']).strip(),
              'license':     ', '.join(pkg_item_map['LICENSE']).strip(),
              'packager':   ', '.join(pkg_item_map['PACKAGER']).strip(),
              'pkg_url':     pkg_item_map['pkg_url']
              }

    if pkg_item_map['URL'] is not None:
        result['url'] = pkg_item_map['URL'][0]

    return result
