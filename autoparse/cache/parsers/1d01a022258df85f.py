import sys
from bs4 import BeautifulSoup

# Чтение HTML из stdin
html = sys.stdin.read()

# Парсинг HTML
soup = BeautifulSoup(html, 'html.parser')

# Извлечение и печать информации
def print_section(title, content):
    print(f"{title}:")
    print(content)
    print()

# Мобильная версия
mobile_switch = soup.find(class_='mobile-switch-notify')
if mobile_switch:
    print_section("Мобильная версия", mobile_switch.get_text(strip=True))

# Реклама
ad_section = soup.find(class_='wb6f5bc57')
if ad_section:
    print_section("Реклама", ad_section.get_text(strip=True))

# Логотип
header_logo = soup.find(class_='header-logo')
if header_logo:
    print_section("Логотип", header_logo.get_text(strip=True))

# Навигация
nav_links = soup.find_all(class_='nav-link')
if nav_links:
    print_section("Навигация", '\n'.join([link.get_text(strip=True) for link in nav_links]))

# Хлебные крошки
breadcrumbs_links = soup.find_all(class_='breadcrumbs-link')
if breadcrumbs_links:
    print_section("Хлебные крошки", ' / '.join([link.get_text(strip=True) for link in breadcrumbs_links]))

# Заголовок страницы
page_title = soup.find(class_='page-title')
if page_title:
    print_section("Заголовок страницы", page_title.get_text(strip=True))

# Вкладки погоды
weathertabs = soup.find_all(class_='weathertab')
if weathertabs:
    print_section("Вкладки погоды", '\n'.join([tab.get_text(strip=True).replace('\n', ' ').strip() for tab in weathertabs]))

# Параметры погоды
weather_parameters = soup.find(class_='widget-weather-parameters')
if weather_parameters:
    print_section("Параметры погоды", weather_parameters.get_text(strip=True).replace('\n', ' ').strip())

# Солнце и Луна
astro_sun = soup.find(class_='astro-sun')
if astro_sun:
    print_section("Солнце", astro_sun.get_text(strip=True).replace('\n', ' ').strip())

astro_moon = soup.find(class_='astro-moon')
if astro_moon:
    print_section("Луна", astro_moon.get_text(strip=True).replace('\n', ' ').strip())

# Новости
news_titles = soup.find_all(class_='rss-card')
if news_titles:
    print_section("Новости", '\n'.join([title.get_text(strip=True) for title in news_titles]))

# Погода на карте
maps_list = soup.find_all(class_='list-item')
if maps_list:
    print_section("Погода на карте", '\n'.join([item.get_text(strip=True) for item in maps_list]))

# Популярные города
popular_cities = soup.find_all(class_='link-hover', href=True)
if popular_cities:
    print_section("Популярные города", '\n'.join([city.get_text(strip=True) for city in popular_cities]))

# Лента новостей
feed_items = soup.find_all(class_='feed-item')
if feed_items:
    print_section("Лента новостей", '\n'.join([item.get_text(strip=True) for item in feed_items]))

# Объясняем.рф
explain_feed_items = soup.find_all(class_='feed-item', href=True)
if explain_feed_items:
    print_section("Объясняем.рф", '\n'.join([item.get_text(strip=True) for item in explain_feed_items]))

# Футер
footer_menu = soup.find_all(class_='footer-item')
if footer_menu:
    print_section("Футер", '\n'.join([item.get_text(strip=True) for item in footer_menu]))

footer_text = soup.find(class_='footer-text')
if footer_text:
    print_section("Футер текст", footer_text.get_text(strip=True))

footer_copy = soup.find(class_='footer-copy')
if footer_copy:
    print_section("Футер копирайт", footer_copy.get_text(strip=True))