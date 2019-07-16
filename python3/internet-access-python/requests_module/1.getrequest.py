import requests

url = 'http://google.com'

response = requests.get(url)

print(response.headers)

## Get requests with query arguments

url2 = 'https://google.com/search?'
query_args = {'q': 'Python tutorials'}

req = requests.get(url2, params=query_args)

print(req.url)
