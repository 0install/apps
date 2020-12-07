#os=Windows
import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from github import tags

releases = [{
    'version': tag['name'].strip('v')
} for tag in tags('hashicorp/vagrant') if not str.startswith(tag['name'], 'v0.') and not str.startswith(tag['name'], 'v1.')]
