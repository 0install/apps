import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import github

releases = [{
    'version': release['tag_name'],
    'released': release['published_at'][0:10]
} for release in github.releases('VSCodium/vscodium') if any(asset["name"].startswith('VSCodium-win32-arm64') for asset in release["assets"])]
