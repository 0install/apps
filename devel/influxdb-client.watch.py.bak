from urllib.request import Request, urlopen
import gzip
import re

req = Request('https://docs.influxdata.com/influxdb/cloud/reference/cli/influx/?t=Linux')
req.add_header('Accept-Encoding', 'gzip')
data = gzip.decompress(urlopen(req).read()).decode('utf-8')
matches = re.search(r'https:\/\/dl.influxdata.com\/influxdb\/releases\/influxdb2-client-([0-9.]+)-linux-amd64\.tar\.gz', data)
releases = [{'version': matches[1]}]
