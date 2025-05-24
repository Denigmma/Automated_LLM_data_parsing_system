import sys
from bs4 import BeautifulSoup

def main():
    # Чтение HTML из stdin
    html = sys.stdin.read()

    # Парсинг HTML
    soup = BeautifulSoup(html, 'html.parser')

    # Извлечение заголовков страниц
    title = soup.find('h1', class_='h1')
    if title:
        print(title.text.strip())

    # Извлечение информации о странах
    countries = {
        'turkey': 'Турция',
        'egypt': 'Египет',
        'abkhazia': 'Абхазия',
        'thailand': 'Таиланд',
        'uae': 'ОАЭ',
        'china': 'Китай',
        'vietnam': 'Вьетнам',
        'maldives': 'Мальдивы',
        'india': 'Индия',
        'sri-lanka': 'Шри-Ланка',
        'georgia': 'Грузия',
        'cuba': 'Куба',
        'armenia': 'Армения',
        'seychelles': 'Сейшелы',
        'russia': 'Россия'
    }

    for country_id, country_name in countries.items():
        country_section = soup.find('h2', class_='wp-block-heading', id=country_id)
        if country_section:
            print(f"\n{country_name}")
            # Описание страны
            description = country_section.find_next('p')
            if description:
                print(f" - Описание: {description.text.strip()}")

            # Популярные курорты
            top_list = country_section.find_next('div', class_='top__list')
            if top_list:
                popular_resorts = top_list.find_all('a')
                if popular_resorts:
                    print(f" - Популярные курорты: {', '.join([resort.text.strip() for resort in popular_resorts])}")

            # Высокий сезон
            high_season = top_list.find_next('p', text=lambda x: x and 'Высокий сезон' in x)
            if high_season:
                print(f" - Высокий сезон: {high_season.text.strip().replace('Высокий сезон ', '')}")

            # Виза
            visa = top_list.find_next('p', text=lambda x: x and ('виза' in x or 'Виза' in x))
            if visa:
                print(f" - Виза: {visa.text.strip()}")

            # Дополнительные ресурсы
            see_also = country_section.find_next('div', class_='see__also')
            if see_also:
                links = see_also.find_all('a')
                if links:
                    print(" - Читайте также:")
                    for link in links:
                        print(f"   - {link.text.strip()}: {link.get('href', '')}")

if __name__ == "__main__":
    main()