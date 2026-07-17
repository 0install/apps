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
            'assets/latest/%d/hotspot?architecture=aarch64&image_type=jdk&os=mac&vendor=eclipse' % feature_version
        )
        if assets:
            # Derive version and build straight from release_name (e.g.
            # "jdk-18.0.2.1+1") so four-component patch releases (18.0.2.1) and
            # bare GA builds ("jdk-21+35") are reproduced exactly as they appear
            # in Adoptium's release tags and asset filenames.
            name = assets[0]['release_name'][len('jdk-'):]
            version, _, build = name.partition('+')
            releases.append({
                'version': version,
                'build': build,
                'major': version.split('.')[0],
            })
    except Exception:
        pass
