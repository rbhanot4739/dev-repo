import requests
from bs4 import BeautifulSoup

req = requests.get('http://www.accuweather.com/en/in/delhi/202396/daily-weather-forecast/202396')
# req = requests.get('http://www.accuweather.com/en/in/delhi/202396/april-weather/202396')
soup = BeautifulSoup(req.text, 'html.parser')

panel = list(soup.find_all('div', {'id': 'feed-tabs'}))

print(soup.find('span', class_='current-city').text, '  ', soup.find('span', class_='local-temp').text)

print(panel[-1].a.text)

data = list(panel[-1].ul.find_all('li'))

for item in data:
    day = item.h3.text
    date = item.h4.text
    max_temp = item.find('span', class_='large-temp').text
    min_temp = item.find('span', class_='small-temp').text
    condition = item.find('span', class_='cond').text
    print(date, day, max_temp, min_temp, condition)
