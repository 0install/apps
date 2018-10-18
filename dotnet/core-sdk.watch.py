from urllib import request
import re

skipped_versions = ['2.1.300', '2.1.301', '2.1.302', '2.1.400', '2.1.401', '2.1.402']

def get(uri):
    return request.urlopen(request.Request(uri, headers={'User-Agent': 'Python'})).read().decode('utf-8')

def handle(version, released):
    def download_uri(arch):
        download_page = get('https://www.microsoft.com/net/download/thank-you/dotnet-sdk-' + version + '-' + arch + '-binaries')
        return re.search('<a href="(https:\/\/download\.visualstudio\.microsoft\.com\/download\/pr\/.*?)"', download_page).group(1)

    return {
        'version': version,
        'released': released,
        'windows-x64-download-uri': download_uri('windows-x64'),
        'windows-x86-download-uri': download_uri('windows-x86'),
        'linux-x64-download-uri': download_uri('linux-x64'),
        'macos-x64-download-uri': download_uri('macos-x64')
    }

data = get('https://www.microsoft.com/net/download/dotnet-core/2.1')
matches = re.findall(r'<p class="mb-5">Released (....-..-..)<\/p>[\S\s]*?\s+<h3 id="sdk-([0-9\.]+)">', data, re.MULTILINE)
releases = [handle(version=match[1], released=match[0]) for match in matches if match[1] not in skipped_versions]