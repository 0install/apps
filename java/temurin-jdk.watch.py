from urllib import request
import json

def adoptium_api(path):
    req = request.Request('https://api.adoptium.net/v3/' + path)
    req.add_header('User-Agent', '0watch')
    return json.loads(request.urlopen(req).read())

available = adoptium_api('info/available_releases')

releases = []
for feature_version in available['available_releases']:
    try:
        assets = adoptium_api(
            'assets/latest/%d/hotspot?architecture=x64&image_type=jdk&os=linux&vendor=eclipse' % feature_version
        )
        if assets:
            version = assets[0]['version']
            releases.append({
                'version': '%d.%d.%d' % (version['major'], version['minor'], version['security']),
                'build': str(version['build']),
                'major': str(version['major']),
            })
    except Exception:
        pass
