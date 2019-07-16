from bs4 import BeautifulSoup as BS

with open('test.xml') as XF:
    data = XF.read()
    soup = BS(data, 'lxml')
    print(soup.find('book', id='bk109'))
