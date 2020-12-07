import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from github import releases
import re

releases = [{
    'version': release['tag_name'].strip('v'),
    'released': release['published_at'][0:10]
} for release in releases('grpc-ecosystem/grpc-gateway') if not 'alpha' in release['tag_name'] and not 'beta' in release['tag_name'] and not 'rc' in release['tag_name'] and len(release['assets']) > 0]
