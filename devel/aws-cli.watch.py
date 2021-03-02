#os=Windows
import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from github import tags

releases = [{
    'version': tag['name']
} for tag in tags('aws/aws-cli') if tag['name'][0:2] == '2.' and tag['name'] != '2.1.29' and not 'dev' in tag['name']]
