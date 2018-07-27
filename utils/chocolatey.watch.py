from urllib import request
from xml.etree import ElementTree

def convert(entry):
    properties = entry.find('{http://schemas.microsoft.com/ado/2007/08/dataservices/metadata}properties')

    prefix = '{http://schemas.microsoft.com/ado/2007/08/dataservices}'
    version = properties.find(prefix + 'Version').text
    return {
        'original-version': version,
        'version': version.replace('beta', 'pre').replace('alpha', 'pre-pre'),
        'released': properties.find(prefix + 'Published').text[0:10],
        'stability': 'testing' if properties.find(prefix + 'IsPrerelease').text == 'true' else 'stable'
    }

data = request.urlopen('https://chocolatey.org/api/v2/Packages()?$filter=(Id%20eq%20%27chocolatey%27)%20and%20(IsApproved%20eq%20true)%20and%20not%20(year(Published)%20eq%201900)').read().decode('utf-8')
releases = [convert(entry) for entry in ElementTree.fromstring(data).findall('{http://www.w3.org/2005/Atom}entry')]
