from urllib import request
import re
from datetime import datetime

data = request.urlopen('https://fossies.org/windows/misc/').read().decode('utf-8')
match = re.findall(r'audacity-([0-9\.]+)\.zip<\/B><\/A> \(([0-9]{1,2} ...)', data)[0]
releases = [{
    'version': match[0],
    'released': datetime.strftime(datetime.strptime(match[1] + ' ' + str(datetime.today().year), '%d %b %Y'), '%Y-%m-%d')
}]
