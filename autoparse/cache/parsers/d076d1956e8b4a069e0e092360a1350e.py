import sys
from bs4 import BeautifulSoup

def main():
    # Чтение HTML из stdin
    html = sys.stdin.read()

    # Парсинг HTML
    soup = BeautifulSoup(html, 'html.parser')

    # Извлечение данных о температуре по часам
    hours = soup.select('section.section-content div.widget-row-datetime-time div.row-item span')
    temperatures_hourly = soup.select('section.section-content div.widget-row-chart div.values div.value temperature-value')

    hourly_data = []
    for hour, temp in zip(hours, temperatures_hourly):
        hourly_data.append(f"{hour.text} - {temp.text}°C")

    # Извлечение данных о температуре на всю неделю
    dates = soup.select('section.section-content div.weathertabs div.weathertab div.tab-content div.date')
    temperatures_weekly = soup.select('section.section-content div.weathertabs div.weathertab div.tab-content div.tab-temp div.values div.value temperature-value')

    weekly_data = []
    for date, temp_min, temp_max in zip(dates, temperatures_weekly[::2], temperatures_weekly[1::2]):
        weekly_data.append(f"{date.text} - {temp_min.text}°C / {temp_max.text}°C")

    # Вывод данных
    print("Температура по часам:")
    for data in hourly_data:
        print(data)

    print("\nТемпература на всю неделю:")
    for data in weekly_data:
        print(data)

if __name__ == "__main__":
    main()