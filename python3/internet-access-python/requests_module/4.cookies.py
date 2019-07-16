import requests
import requests.cookies

url = 'http://httpbin.org/cookies'

jar = requests.cookies.RequestsCookieJar()
jar.set('first cookie', 'first', domain='httpbin.org', path='/cookies')
jar.set('2nd cookie', 'first', domain='httpbin.org')

r = requests.get(url, cookies=jar)
r.raise_for_status()
print(r.text)
