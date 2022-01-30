import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import github, re

releases = [{
    'version': release['tag_name'].strip('v'),
    'released': release['published_at'][0:10]
} for release in github.releases('grpc-ecosystem/grpc-gateway') if not 'alpha' in release['tag_name'] and not 'beta' in release['tag_name'] and not 'rc' in release['tag_name'] and release['assets']]
