import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import github

excluded_versions = ['1.7.8', '1.7.12']

releases = [{
    'version': tag['name']
} for tag in github.tags('mpc-hc/mpc-hc') if not '_' in tag['name'] and not tag['name'] in excluded_versions]
