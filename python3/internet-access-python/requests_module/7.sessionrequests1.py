import requests

s = requests.Session()
s.cookies.update({'Industry': 'IT', 'Domain': 'Programming'})

r1 = s.get('http://httpbin.org/cookies')
print(r1.text)

r2 = s.get('http://httpbin.org/cookies', cookies={'Language': 'Python', 'ver': '3.6'})
print(r2.text)

r3 = s.get('http://httpbin.org/cookies', cookies={'Industry': 'Media', 'Domain': 'Audio Engineering'})
print(r3.text)

r4 = s.get('http://httpbin.org/cookies')
print(r4.text)
