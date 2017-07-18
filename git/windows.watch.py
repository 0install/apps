from urllib import request
import json

def convert(release):
    tag = release['tag_name']
    main_version = tag[1:tag.rfind('windows.')-1]
    build = tag[tag.rfind('windows.')+8:]
    version = main_version if build == '1' else tag[1:].replace('windows.', '')
    released = release['published_at'][0:10]
    return {'version': version, 'main-version': main_version, 'build': build, 'released': released}

data = request.urlopen('https://api.github.com/repos/git-for-windows/git/releases').read()
releases = [convert(release) for release in json.loads(data) if not release['prerelease']]
