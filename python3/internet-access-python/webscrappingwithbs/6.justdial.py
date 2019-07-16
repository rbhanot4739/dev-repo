import requests
from bs4 import BeautifulSoup as bs

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36'}

url = 'https://www.justdial.com/Noida/coffee shops'
r = requests.get(url, headers=headers)
r.raise_for_status()
soup = bs(r.content, 'html.parser')

details = soup.find_all('div', class_='col-sm-5 col-xs-8 store-details sp-detail paddingR0')

for detail in details:
    print('\n')
    title = detail.h4.text.strip()
    rating = detail.find('span', class_="exrt_count").text
    distance = detail.find('span', class_='dist dist-phone').span.text
    phone = detail.find('p', class_='contact-info').text.strip()
    address = detail.find('p', class_='address-info tme_adrssec').find('span', class_='mrehover dn').text.strip()

    print('{} (Within {})\nRating : {}\nPhone Number: {}\nAddress : {}'.format(title, distance, rating, phone, address))
