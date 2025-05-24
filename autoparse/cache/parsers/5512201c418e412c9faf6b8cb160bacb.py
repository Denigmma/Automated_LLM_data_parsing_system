import sys
from bs4 import BeautifulSoup

def main():
    # Чтение HTML из stdin
    html_content = sys.stdin.read()

    # Парсинг HTML
    soup = BeautifulSoup(html_content, 'html.parser')

    # Извлечение заголовка статьи
    title_block = soup.select_one('article.col-12.col-lg-9.col-xl-8 div.mb-4 mb-lg-5 h1')
    if title_block:
        print(f"# {title_block.text.strip()}")

    # Основной контент статьи
    content_block = soup.select_one('article.col-12.col-lg-9.col-xl-8 div.hexlet-blog-post-body')
    if content_block:
        # Извлечение разделов статьи
        for section in content_block.find_all('h2'):
            print(f"\n## {section.text.strip()}")

        # Извлечение подразделов статьи
        for subsection in content_block.find_all('h3'):
            print(f"\n### {subsection.text.strip()}")

        # Извлечение параграфов
        for paragraph in content_block.find_all('p'):
            print(paragraph.text.strip())

        # Извлечение списков
        for ul in content_block.find_all('ul'):
            for li in ul.find_all('li'):
                print(f"- {li.text.strip()}")

if __name__ == "__main__":
    main()