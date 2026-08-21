from urllib import request
import json


PLATFORMS = (
    ('x64', 'windows'),
    ('x64', 'linux'),
    ('aarch64', 'linux'),
    ('x64', 'mac'),
    ('aarch64', 'mac'),
)


def adoptium_api(path):
    req = request.Request('https://api.adoptium.net/v3/' + path)
    req.add_header('User-Agent', '0watch')
    return json.loads(request.urlopen(req).read())


def get_common_release_name(feature_version):
    platform_releases = []
    for architecture, operating_system in PLATFORMS:
        releases = adoptium_api(
            'assets/feature_releases/%d/ga?architecture=%s&image_type=jdk&jvm_impl=hotspot&os=%s&vendor=eclipse'
            % (feature_version, architecture, operating_system)
        )
        release_names = [release['release_name'] for release in releases]
        if not release_names:
            return None
        platform_releases.append(release_names)

    common_releases = set(platform_releases[0])
    for release_names in platform_releases[1:]:
        common_releases &= set(release_names)

    for release_name in platform_releases[0]:
        if release_name in common_releases:
            return release_name

    return None


available = adoptium_api('info/available_releases')

releases = []
for feature_version in available['available_releases']:
    try:
        name = get_common_release_name(feature_version)
        if name:
            # Derive version and build straight from release_name (e.g.
            # "jdk-18.0.2.1+1") so four-component patch releases (18.0.2.1) and
            # bare GA builds ("jdk-21+35") are reproduced exactly as they appear
            # in Adoptium's release tags and asset filenames.
            name = name[len('jdk-'):]
            version, _, build = name.partition('+')
            releases.append({
                'version': version,
                'build': build,
                'major': version.split('.')[0],
            })
    except Exception:
        pass
