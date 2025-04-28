from urllib import request
import json

excluded_versions = []
data = request.urlopen('https://fastapi.metacpan.org/v1/release/Parallel-ForkManager').read().decode('utf-8')
release = json.loads(data)
releases = [{   'version': release['version'], 
                'released': release['date'].split('T')[0], 
                'name': release['distribution'], 
                'summary': release['abstract'], 
                'url': release['download_url'],
                'creator': release['author']
            }]
