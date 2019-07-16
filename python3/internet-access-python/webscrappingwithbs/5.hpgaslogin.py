import requests, re
from bs4 import BeautifulSoup as bs
import sys

# url = 'http://testing-ground.scraping.pro/login'
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36'}

param1 = sys.argv[1]
param2 = sys.argv[2]

url2 = 'https://myhpgas.in/myHPGas/Login.aspx'

with requests.Session() as s:
    s.headers.update(headers)
    page_html = s.get(url2).text

    tsmManagerHiddenField = re.search(r'id="tsmManager_HiddenField" value="(.*)"', page_html).group(1)
    eventArgument = re.search(r'id="__EVENTARGUMENT" value="(.*)"', page_html).group(1)
    eventTarget = re.search(r'id="__EVENTTARGET" value="(.*)"', page_html).group(1)
    lastFocus = re.search(r'id="__LASTFOCUS" value="(.*)"', page_html).group(1)
    viewState = re.search(r'id="__VIEWSTATE" value="(.*)"', page_html).group(1)
    eventValidation = re.search(r'id="__EVENTVALIDATION" value="(.*)"', page_html).group(1)

    payload = {'__EVENTARGUMENT': eventArgument, '__EVENTTARGET': eventTarget, '__EVENTVALIDATION': eventValidation,
               '__LASTFOCUS': lastFocus, '__VIEWSTATE': viewState, 'ctl00$ContentPlaceHolder1$txtUserNameEmail': param1,
               'ctl00$ContentPlaceHolder1$txtPassword': param2, 'ctl00$ContentPlaceHolder1$btnLogin': 'Login',
               'ctl00$ddlSelectLanguage': '-1', 'tsmManager_HiddenField': tsmManagerHiddenField}

    p = s.post(url2, data=payload)
    p.raise_for_status()
    r = s.get('https://myhpgas.in/myHPGas/HPGas/User/ConsumerConsole.aspx')
    soup = bs(r.content, 'html.parser')
    print(soup.get_text())
