import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import github, re

def releases(fileExt):
    for release in github.releases('Studio3T/robomongo'):
        if not release['prerelease']:
            for asset in release['assets']:
                if asset['name'].endswith(fileExt):
                   yield {
                        'version': release['tag_name'].strip('v'),
                        'released': release['published_at'][0:10],
                        'commit': re.search(r'-([0-9a-f]+)' + re.escape(fileExt), asset['name']).group(1)
                    }
