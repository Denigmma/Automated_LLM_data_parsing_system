import sys
from bs4 import BeautifulSoup

def main():
    # Чтение HTML из stdin
    html = sys.stdin.read()

    # Парсинг HTML
    soup = BeautifulSoup(html, 'html.parser')

    # Температура по часам
    hourly_temps = soup.select('.widget-row-chart.widget-row-chart-temperature-air .values temperature-value')
    hourly_times = soup.select('.widget-row-datetime-time .row-item span')

    hourly_data = []
    for time, temp in zip(hourly_times, hourly_temps):
        hourly_data.append(f"{time.text} - {temp.text}")

    # Температура на неделю
    weekly_temps = soup.select('.weathertab-wrap .tab-temp .values temperature-value')
    weekly_days = soup.select('.weathertab-wrap .date')

    weekly_data = []
    for day, temp in zip(weekly_days, weekly_temps):
        weekly_data.append(f"{day.text} - {temp.text}")

    # Вывод данных
    print("Температура по часам:")
    for data in hourly_data:
        print(data)

    print("\nТемпература на неделю:")
    for data in weekly_data:
        print(data)

if __name__ == "__main__":
    main()