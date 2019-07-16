import urllib.request
import urllib.parse
import re

url = 'https://wiki.python.org/moin/BeginnersGuide/Programmers'
values = {'p': 'Django'}
data = urllib.parse.urlencode(values).encode('utf-8')
data = ''

headers = {}
headers['User-Agent'] = "Mozilla/5.0"
req = urllib.request.Request(url + '?' + str(data), headers=headers)
resp = urllib.request.urlopen(req).read().decode('utf-8')

content = re.sub(r'<.*?>', '', resp)

print(content)
