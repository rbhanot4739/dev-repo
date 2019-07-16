import requests
from bs4 import BeautifulSoup as BS

try:
    req = requests.get(
        'https://www.skymetweather.com/forecast/weather/india/delhi/new%20delhi/new%20delhi/extended-forecast',
        timeout=10)
    soup = BS(req.text, 'html.parser')

except Exception as e:
    print('Oops something went wrong \n {}'.format(e))

# print(soup.prettify()) # Used to print neat and formatted HTML code

header_div = soup.find_all('div', class_='SectionTitle')
header_text = header_div[1].text

day_data = soup.find_all('div', {'class': 'forecastBox w23p ml2p'})

print('{:<15s}{:<15s}{:<30s}{:7s}/{:<20s}{:<16s}{:>13s}{:>27s}\n'.format('Day', 'Date', 'Condition', 'Max Temp',
                                                                         'Min Temp', 'Wind Speed', 'RH Factor',
                                                                         'Rain(Chances/Amount)'))

for item in day_data:
    fcHeading = item.find(class_='forecastHeading').text.strip()
    fcDate = item.find(class_='fcDate').text.strip()
    fcCondition = item.find(class_='fcConditionText').text.strip()
    maxTemp = item.find(class_='fcTemperature').find_all(class_='c')[0].text.strip()
    minTemp = item.find(class_='fcTemperature').find_all(class_='c')[-1].text.strip()
    windSpeed = item.find(class_='fcWind fcItem').find(class_='fcRight').text.strip()
    relativeHumidity = item.find(class_='fchumidity fcItem').find(class_='fcRight').text.strip()
    rain = item.find(class_='fcRain fcItem').find(class_='fcRight').text.strip()
    print('{:<15s}{:<15s}{:<30s}{:>8s}/{:<20s}{:<20s}{:>10s}{:>20s}'.format(fcHeading, fcDate, fcCondition, maxTemp,
                                                                            minTemp, windSpeed, relativeHumidity, rain))
