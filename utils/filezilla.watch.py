from urllib import request
import re

data = request.urlopen('https://filezilla-project.org/versions.php').read().decode('utf-8')
matches = re.findall(r'<h3>([0-9\.]+) \((....-..-..)\)</h3>', data)
releases = [{'version': match[0], 'released': match[1]} for match in matches if match[0][0:4] != '3.0.']
