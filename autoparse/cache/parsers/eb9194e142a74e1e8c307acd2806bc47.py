import sys
from bs4 import BeautifulSoup

# Чтение HTML из stdin
html = sys.stdin.read()

# Парсинг HTML с помощью BeautifulSoup
soup = BeautifulSoup(html, 'html.parser')

# Извлечение информации о текущей погоде
weather_block = soup.find('a', class_='weathertab', href='/weather-sankt-peterburg-4079/now/')

if weather_block:
    weather_value = weather_block.find('temperature-value')
    if weather_value:
        temperature = weather_value.text.strip()
        feel_like_block = weather_block.find('div', class_='weather-feel')
        feel_like_value = feel_like_block.find('temperature-value') if feel_like_block else None
        feel_like = feel_like_value.text.strip() if feel_like_value else 'Нет данных'

        print(f'Текущая температура: {temperature}°C')
        print(f'По ощущению: {feel_like}°C')
    else:
        print('Не удалось извлечь данные о текущей погоде.')
else:
    print('Не удалось найти блок с текущей погодой.')