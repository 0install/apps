import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import github

releases = [{
    'version': release['tag_name'],
    'released': release['published_at'][0:10],
} for release in github.releases('ungoogled-software/ungoogled-chromium-portablelinux')
   if not release['prerelease'] and any(asset['name'].endswith('-x86_64_linux.tar.xz') for asset in release['assets'])]
