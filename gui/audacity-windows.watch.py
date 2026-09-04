#os=Windows
import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import github

def convert(release):
    original_version = release['tag_name'][len('Audacity-'):]
    version = original_version.replace('-beta', '-pre')
    released = release['published_at'][0:10]
    stability = 'testing' if release['prerelease'] else 'stable'
    return {'version': version, 'released': released, 'stability': stability}

def major_version(tag_name):
    return int(tag_name[len('Audacity-'):].split('.')[0])

releases = [convert(release) for release in github.releases('audacity/audacity')
    if not release['prerelease'] and major_version(release['tag_name']) >= 4
    and any(asset['name'].endswith('.msi') for asset in release['assets'])]
