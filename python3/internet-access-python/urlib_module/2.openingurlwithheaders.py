import urllib.request
import urllib.parse

# values = {'q':'Python Tutorials'}
values = {'s': 'basic', 'submit': 'search'}
data = urllib.parse.urlencode(values).encode('utf-8')
print(data)
# url = 'http://google.com/search?'+data
url = 'http://pythonprogramming.net'

headers = {}
headers['User-Agent'] = "Mozilla/5.0"
req = urllib.request.Request(url, data, headers=headers)
print(req.get_method())
resp = urllib.request.urlopen(req)  # print(resp.read())
