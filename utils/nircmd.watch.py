from urllib import request
import re
import datetime

data = request.urlopen('http://www.nirsoft.net/utils/nircmd.html').read().decode('utf-8')
matches = re.findall(r'<tr><td>(\d\d/\d\d/\d\d\d\d)<td>(\d.\d+)<td>', data)
date = datetime.datetime.strptime(matches[0][0], '%d/%m/%Y').strftime('%Y/%m/%d')

releases = [{'version': matches[0][1], 'released': date}]
