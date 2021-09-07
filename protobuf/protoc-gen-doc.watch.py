import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import github, re

releases = [{
    'version': release['tag_name'].strip('v'),
    'go-version': re.findall(r'go([\d\.]+)\.tar\.gz', release['assets'][0]['name'])[0],
    'released': release['published_at'][0:10]
} for release in github.releases('pseudomuto/protoc-gen-doc') if not release['prerelease'] and '.go' in release['assets'][0]['name']]
