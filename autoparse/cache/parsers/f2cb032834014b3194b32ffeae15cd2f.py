import sys
from bs4 import BeautifulSoup

def main():
    # Чтение HTML из stdin
    html = sys.stdin.read()

    # Парсинг HTML
    soup = BeautifulSoup(html, 'html.parser')

    # Извлечение последних 5 новостей
    news_items = soup.find_all('div', class_='cell-list__item', limit=5)

    # Печать информации о каждой новости
    for index, item in enumerate(news_items, start=1):
        print(f"Новость {index}:")

        title_tag = item.find('span', class_='cell-list__item-title')
        if title_tag:
            print(f"Заголовок: {title_tag.get_text(strip=True)}")

        date_tag = item.find('div', class_='cell-info__date')
        if date_tag:
            print(f"Дата: {date_tag.get_text(strip=True)}")

        link_tag = item.find('a', class_='cell-list__item-link')
        if link_tag:
            print(f"Ссылка: {link_tag.get('href', '')}")

        print()  # Пустая строка для разделения новостей

if __name__ == "__main__":
    main()