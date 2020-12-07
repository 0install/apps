import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from github import tags

releases = [{
    'version': tag['name'].strip('v')
} for tag in tags('Microsoft/vscode') if not '/' in tag['name'] and not 'GOOD' in tag['name'] and not 'BAD' in tag['name'] and not 'bad' in tag['name'] and not 'conflict' in tag['name'] and not 'vsda' in tag['name'] and tag['name'] != '1.999.0']
