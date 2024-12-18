from urllib import request
import re
from datetime import datetime

data = request.urlopen('https://services.gradle.org/distributions/').read().decode('utf-8')
matches = re.findall(r'<span class="name">gradle-([0-9\.\-milestonerc]+)-bin.zip<\/span>\n\s+<span class="date">(..-...-....)', data)
releases = [{
    'version': match[0].replace('milestone', 'pre'),
    'version-original': match[0],
    'stability': 'developer' if 'milestone' in match[0] else ('testing' if 'rc' in match[0] else 'stable'),
    'released': datetime.strftime(datetime.strptime(match[1], '%d-%b-%Y'), '%Y-%m-%d')
} for match in matches]
