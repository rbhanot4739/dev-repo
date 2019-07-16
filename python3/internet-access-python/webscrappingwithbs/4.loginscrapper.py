import requests, re
from bs4 import BeautifulSoup as bs
import sys

url = 'http://testing-ground.scraping.pro/login'
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36'}

with requests.Session() as s:
    s.get(url)
    s.headers.update(headers)
    payload = {'usr': 'admin', 'pwd': '12345'}
    query = {'mode': 'login'}
    p = s.post(url, data=payload, params=query)
    # print('****',p.history)
    # print(p.status_code)
    p.raise_for_status()
    soup = bs(p.content, 'html.parser')
    print(soup.get_text())
