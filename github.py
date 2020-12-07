# Helpers for listing tags and releases on GitHub repositories.

from urllib import request
import os, json

def tags(repo):
    return api('repos/' + repo + '/tags')

def releases(repo):
    return api('repos/' + repo + '/releases')

def api(uri):
    token = os.getenv('GITHUB_TOKEN')
    headers={}
    if token:
        headers['Authorization'] = 'token ' + token

    response = request.urlopen(request.Request('https://api.github.com/' + uri, headers=headers)).read()
    return json.loads(response)
