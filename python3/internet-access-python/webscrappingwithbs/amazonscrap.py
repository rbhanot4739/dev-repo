import requests
from bs4 import BeautifulSoup as bs

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36'}
url = 'http://www.amazon.in/s/ref=nb_sb_ss_i_6_4?url=search-alias%3Daps&field-keywords=headphones+with+mic&sprefix=Head%2Caps%2C331&crid=2BOJLGQ1RZJFO'

html = requests.get(url, headers=headers)

soup = bs(html.content, 'html.parser')
items = soup.find_all('div', class_='s-item-container')

for item in items:
    try:
        p_name = item.h2.text
        orig_price = item.find('span', class_='a-size-small a-color-secondary a-text-strike').text.strip()
        dis_price = item.find('span', class_='a-size-base a-color-price s-price a-text-bold').text.strip()
        delivery = item.find('div', class_='a-row a-spacing-top-mini a-spacing-mini').text.strip()
        rating = item.find('i', class_='a-icon a-icon-star a-star-4').text.strip()
        discount = 100 - ((float(''.join((dis_price.split(',')))) / float(''.join((orig_price.split(','))))) * 100)
        print(
            '{} ({})\n{} ({}) at {:2.0f}% off\n{}\n'.format(p_name, rating, dis_price, orig_price, discount, delivery))

    except Exception as e:
        pass
