from urllib import request
import re

def get(uri):
    return request.urlopen(request.Request(uri, headers={'User-Agent': 'Python'})).read().decode('utf-8')

def handle(version, released):
    def download_uri(arch):
        download_page = get('https://www.microsoft.com/net/download/thank-you/dotnet-runtime-' + version + '-' + arch + '-binaries')
        return re.search('<a href="(https:\/\/download\..*?)"', download_page).group(1)

    return {
        'version': version,
        'released': released,
        'windows-x64-download-uri': download_uri('windows-x64'),
        'windows-x86-download-uri': download_uri('windows-x86'),
        'linux-x64-download-uri': download_uri('linux-x64'),
        'macos-x64-download-uri': download_uri('macos-x64')
    }

def get_releases(major_version):
    data = get('https://www.microsoft.com/net/download/dotnet-core/' + major_version)
    matches = re.findall(r'<h2 class="h3"><text>v<\/text>([0-9\.]+)<\/h2>[\S\s]*?\s+<p class="mb-5">Released (....-..-..)<\/p>', data, re.MULTILINE)
    return [handle(version=match[0], released=match[1]) for match in matches if match[0]]

releases = get_releases('2.1') + get_releases('2.2') + get_releases('3.0')
