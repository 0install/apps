#os=Windows
import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import github

releases = [{
    'version': release['tag_name'][len('azure-cli-'):],
    'released': release['published_at'][0:10]
} for release in github.releases('Azure/azure-cli') if not release['prerelease'] and int(release['published_at'][0:4]) >= 2020 and len(release['assets']) > 0]
