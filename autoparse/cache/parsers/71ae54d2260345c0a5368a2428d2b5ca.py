import sys
from bs4 import BeautifulSoup

def main():
    # Чтение HTML из stdin
    html = sys.stdin.read()

    # Парсинг HTML с помощью BeautifulSoup
    soup = BeautifulSoup(html, 'html.parser')

    # Извлечение информации о последних новостях
    news_blocks = soup.find_all('div', class_='lenta__item')

    if news_blocks:
        print("Последние новости:")
        for index, block in enumerate(news_blocks, start=1):
            date_block = block.find('span', class_='lenta__item-date')
            text_block = block.find('span', class_='lenta__item-text')
            link_block = block.find('a', class_='lenta__item-size', href=True)

            date = date_block.get_text(strip=True) if date_block else 'Нет даты'
            text = text_block.get_text(strip=True) if text_block else 'Нет текста'
            link = link_block.get('href', '') if link_block else '#'

            print(f"{index}. {date} {text} ([Полная новость]({link}))")
    else:
        print("Новости не найдены.")

if __name__ == "__main__":
    main()