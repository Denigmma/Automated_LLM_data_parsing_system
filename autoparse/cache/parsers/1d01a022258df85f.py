import sys
from bs4 import BeautifulSoup

def main():
    # Чтение HTML из stdin
    html_content = sys.stdin.read()

    # Парсинг HTML с помощью BeautifulSoup
    soup = BeautifulSoup(html_content, 'html.parser')

    # Извлечение и печать всех заголовков
    headings = soup.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6'])
    if headings:
        print("Заголовки:")
        for heading in headings:
            print(heading.get_text(strip=True))
    else:
        print("Не найдены заголовки")

    # Извлечение и печать всех ссылок
    links = soup.find_all('a')
    if links:
        print("\nСсылки:")
        for link in links:
            href = link.get('href', '')
            text = link.get_text(strip=True)
            print(f"{text}: {href}")
    else:
        print("Не найдены ссылки")

    # Извлечение и печать всех изображений
    images = soup.find_all('img')
    if images:
        print("\nИзображения:")
        for img in images:
            src = img.get('src', '')
            alt = img.get('alt', '')
            print(f"{alt}: {src}")
    else:
        print("Не найдены изображения")

    # Извлечение и печать всех кнопок
    buttons = soup.find_all('button')
    if buttons:
        print("\nКнопки:")
        for button in buttons:
            text = button.get_text(strip=True)
            print(text)
    else:
        print("Не найдены кнопки")

    # Извлечение и печать всех элементов с классом 'weather-icon-group'
    weather_icons = soup.find_all(class_='weather-icon-group')
    if weather_icons:
        print("\nИконки погоды:")
        for icon in weather_icons:
            print(icon.get_text(strip=True))
    else:
        print("Не найдены иконки погоды")

    # Извлечение и печать всех элементов с классом 'temperature-value'
    temperatures = soup.find_all(class_='temperature-value')
    if temperatures:
        print("\nТемпературы:")
        for temp in temperatures:
            print(temp.get_text(strip=True))
    else:
        print("Не найдены температуры")

    # Извлечение и печать всех элементов с классом 'speed-value'
    speeds = soup.find_all(class_='speed-value')
    if speeds:
        print("\nСкорости ветра:")
        for speed in speeds:
            print(speed.get_text(strip=True))
    else:
        print("Не найдены скорости ветра")

    # Извлечение и печать всех элементов с классом 'precipitation'
    precipitations = soup.find_all(class_='precipitation')
    if precipitations:
        print("\nОсадки:")
        for precipitation in precipitations:
            print(precipitation.get_text(strip=True))
    else:
        print("Не найдены осадки")

    # Извлечение и печать всех элементов с классом 'feed-item'
    feed_items = soup.find_all(class_='feed-item')
    if feed_items:
        print("\nЭлементы ленты новостей:")
        for item in feed_items:
            link = item.find('a')
            if link:
                href = link.get('href', '')
                text = link.get_text(strip=True)
                print(f"{text}: {href}")
    else:
        print("Не найдены элементы ленты новостей")

    # Извлечение и печать всех элементов с классом 'breadcrumbs-link'
    breadcrumbs = soup.find_all(class_='breadcrumbs-link')
    if breadcrumbs:
        print("\nХлебные крошки:")
        for breadcrumb in breadcrumbs:
            href = breadcrumb.get('href', '')
            text = breadcrumb.get_text(strip=True)
            print(f"{text}: {href}")
    else:
        print("Не найдены хлебные крошки")

    # Извлечение и печать всех элементов с классом 'astro-times'
    astro_times = soup.find_all(class_='astro-times')
    if astro_times:
        print("\nАстрономические времена:")
        for time in astro_times:
            print(time.get_text(strip=True))
    else:
        print("Не найдены астрономические времена")

if __name__ == "__main__":
    main()