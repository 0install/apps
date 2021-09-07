#os=Windows
import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import github

releases = [{
    'version': tag['name'].strip('v')
} for tag in github.tags('hashicorp/vagrant') if not str.startswith(tag['name'], 'v0.') and not str.startswith(tag['name'], 'v1.')]
