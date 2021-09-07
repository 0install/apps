#os=Windows
import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import github

def convert(release):
    tag = release['tag_name']
    main_version = tag[1:tag.rfind('windows.')-1]
    build = tag[tag.rfind('windows.')+8:]
    version = main_version if build == '1' else tag[1:].replace('windows.', '')
    released = release['published_at'][0:10]
    return {'version': version, 'main-version': main_version, 'build': build, 'released': released}

releases = [convert(release) for release in github.releases('git-for-windows/git') if not release['prerelease']]
