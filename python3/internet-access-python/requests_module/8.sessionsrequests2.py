import requests

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:53.0) Gecko/20100101 Firefox/53.0'}
get_r = requests.get('http://requestb.in/17or4911', timeout=7, headers=headers)

print(get_r.request.headers, '\n')
print(get_r.headers, '\n')

post_r = requests.post('http://requestb.in/14ietog1', data={"key1": 'value1'})

post_r.raise_for_status()
print(post_r.request.headers, '\n')
print(post_r.headers, '\n')

with requests.Session() as s:
    s.headers.update({'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:53.0) Gecko/20100101 Firefox/53.0'})
    get_r2 = s.get('http://requestb.in/17or4911')
    # Analysing the session headers and response cookie
    print(get_r2.request.headers, '\n')
    print(get_r2.headers, '\n')

    post_r2 = s.post('http://requestb.in/14ietog1', data={"key2": 'value2'})
    # Analysing Request headers
    print(post_r2.request.headers, '\n')
    # Analysing Response headers
    print(post_r2.headers, '\n')
