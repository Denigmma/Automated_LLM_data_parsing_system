import sys
from bs4 import BeautifulSoup

# Чтение HTML из stdin
html = sys.stdin.read()

# Парсинг HTML
soup = BeautifulSoup(html, 'html.parser')

# Извлечение данных из заголовка
header = soup.find('header', class_='styles_header__du6tb')
logo = header.find('a', class_='styles_logo-header__link__o2Vj3')
logo_href = logo['href']
logo_imgs = logo.find_all('img')
logo_desktop_src = logo_imgs[0]['src']
logo_mobile_src = logo_imgs[1]['src']

print(f"Логотип: {logo_href}")
print(f"Источник логотипа для десктопа: {logo_desktop_src}")
print(f"Источник логотипа для мобильных устройств: {logo_mobile_src}")

# Извлечение ссылок из навигационного меню
nav_links = header.find('nav', class_='styles_top-menu__X9Ebw').find_all('a', class_='styles_top-menu__link__GMlA4')
print("\nНавигационное меню:")
for link in nav_links:
    print(f"{link.text}: {link['href']}")

# Извлечение информации о книге
book_cover = soup.find('section', class_='styles_bookCover__GY1Dr')
book_title = book_cover.find('h1', class_='styles_title___Pe88').text
book_description = book_cover.find('p', class_='styles_description__TW7TQ').text
print("\nИнформация о книге:")
print(f"Название: {book_title}")
print(f"Описание: {book_description}")

# Извлечение содержания книги
book_contents = soup.find('ul', class_='styles_book-contents__a6F2_')
print("\nСодержание книги:")
for chapter in book_contents.find_all('li', recursive=False):
    chapter_title = chapter.find('h2', class_='styles_title__ieO3h').text
    print(f"\n{chapter_title}")
    for subchapter in chapter.find_all('li'):
        subchapter_number = subchapter.find('span', class_='styles_article-number__TfJBt').text
        subchapter_title = subchapter.find('span', class_='styles_title__y8AzO').text
        subchapter_link = subchapter.find('a', class_='styles_link__zNsNu')['href']
        print(f"{subchapter_number} {subchapter_title}: {subchapter_link}")

# Извлечение информации из подвала
footer = soup.find('footer', class_='styles_footer__SuJ_W')
footer_links = footer.find_all('a')
print("\nСсылки в подвале:")
for link in footer_links:
    print(f"{link.text}: {link['href']}")

# Извлечение информации о сообществе
call_to_action = soup.find('section', class_='styles_callToAction__XgopL')
community_title = call_to_action.find('h3', class_='styles_title__jT8cm').text
community_description = call_to_action.find('span', class_='styles_description__BxoL_').text
community_link = call_to_action.find('a', class_='styles_action-link__ZwQwM')['href']
print("\nПризыв к действию:")
print(f"Заголовок: {community_title}")
print(f"Описание: {community_description}")
print(f"Ссылка: {community_link}")

# Извлечение информации о социальных сетях
social_links = soup.find('ul', class_='styles_socials__DbhxX').find_all('a')
print("\nСоциальные сети:")
for link in social_links:
    social_title = link['title']
    social_href = link['href']
    print(f"{social_title}: {social_href}")