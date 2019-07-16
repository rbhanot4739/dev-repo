import requests

url = 'http://google.com'

req1 = requests.get(url)
req2 = requests.get(url, allow_redirects=False)

print(req1.url)
print(req1.status_code)
print(req1.history)

print(req2.url)
print(req2.status_code)
print(req2.history)
