import urllib.request

url = 'http://google.com'
response = urllib.request.urlopen(url)

headers = response.info()
print(headers)

for line in response:
    print(line)  # print(response.read())
