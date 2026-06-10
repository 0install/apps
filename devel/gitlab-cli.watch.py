from urllib import request
import json

def has_binaries(release):
    return any(link['name'].endswith(('.tar.gz', '.zip')) and 'source' not in link['name']
               for link in release.get('assets', {}).get('links', []))

releases = []
page = 1
while True:
    url = 'https://gitlab.com/api/v4/projects/gitlab-org%2Fcli/releases?per_page=100&page=' + str(page)
    batch = json.loads(request.urlopen(url).read())
    if not batch:
        break
    for release in batch:
        if release.get('upcoming_release') or not has_binaries(release):
            continue
        releases.append({
            'version': release['tag_name'].lstrip('v'),
            'released': release['released_at'][0:10]
        })
    page += 1
