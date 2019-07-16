import requests

url = 'http://httpbin.org/post'

query_args = {'key1': 'value1', 'key2': 'value2'}

r = requests.post(url, data=query_args)

r.raise_for_status()
print(r.text)
