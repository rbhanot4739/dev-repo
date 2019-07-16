import requests
from bs4 import BeautifulSoup

req = requests.get('http://dataquestio.github.io/web-scraping-pages/simple.html')
soup = BeautifulSoup(req.content, 'html.parser')

# print(soup.prettify())
html = list(soup.children)[2]
body = list(html.children)[3]
p = list(body.children)[1]
# print(p.get_text())

# Finding all instances of a tag at once
print(soup.find_all('p'))
