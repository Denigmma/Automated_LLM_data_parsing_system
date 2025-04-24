from bs4 import BeautifulSoup
from mistralai import Mistral
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
import subprocess
import sys
import re


def clean_html_for_llm(html: str) -> str:
    soup = BeautifulSoup(html, "html.parser")

    # Удаляем служебные и рекламные блоки
    blacklist_classes = [
        "header", "footer", "nav", "navbar", "breadcrumbs", "sidebar",
        "adfox", "media-top", "media-right", "media-bottom", "advert",
        "subscription", "cookie", "popup", "banner", "tracker", "metrika",
        "header__bottom", "header__top", "footer__inner", "footer__menu"
    ]

    # Удаляем по классам
    for cls in blacklist_classes:
        for tag in soup.select(f'.{cls}'):
            tag.decompose()

    # Удаляем нежелательные теги полностью
    for tag_name in ["script", "style", "noscript", "svg", "link", "meta","head",]:
        for tag in soup.find_all(tag_name):
            tag.decompose()

    # Удаляем head целиком (можно оставить, если нужен для структуры)
    head_tag = soup.find("head")
    if head_tag:
        head_tag.decompose()

    # Удаляем комментарии
    for comment in soup.find_all(string=lambda text: isinstance(text, type(soup.comment))):
        comment.extract()

    # Очищаем лишние пустые div
    for div in soup.find_all("div"):
        if not div.get_text(strip=True) and not div.find("img") and not div.find("iframe"):
            div.decompose()

    for tag in soup.find_all():
        # смотрим только непосредственные потомки
        direct_links = [c for c in tag.find_all('a', recursive=False)]
        own_text = tag.get_text(strip=True)
        # если минимум 5 прямых <a> и мало сопутствующего текста
        if len(direct_links) >= 5 and len(own_text) < len(direct_links) * 20:
            tag.decompose()

    # Возвращаем красивый HTML
    return soup.prettify()

# --- Этап 1: Получение HTML через Selenium ---
def get_rendered_html(url, timeout=10):
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--window-size=1920,1080")

    driver = webdriver.Chrome(options=options)
    try:
        driver.get(url)
        WebDriverWait(driver, timeout).until(
            lambda d: d.execute_script("return document.readyState") == "complete"
        )
        return driver.page_source
    finally:
        driver.quit()


# --- Этап 2: Генерация парсера с помощью Mistral ---
def generate_parser(html_content, api_key):
    client = Mistral(api_key=api_key)

    system_prompt = """
        Ты опытный Python-разработчик, специалист по парсингу HTML.
        Твоя задача — создавать работающие Python-скрипты, которые:
        - читают HTML через `sys.stdin`
        - парсят данные через `BeautifulSoup` из `bs4` и стандартные библиотеки,
        - извлекают и печатают всю информацию с HTML, которую человек может узнать на странице.
        - Строго работай с предоставленной HTML-разметкой, не выдумывай классы, которых там нет.
        
        Важно:
        - Не используй фразы "например", "может быть", "если", "предположим"
        - Не выдумывай селекторы — используй только то, что действительно видно в HTML
        - Обязательно добавляй `print(...)` с разумными результатами
    """

    prompt = f"""
    Вот HTML, полученный с сайта. Напиши реальный рабочий скрипт на Python,
    который извлекает и выводит всю доступную информацию на странице.

    Условия:
    - используй только `bs4` и стандартные библиотеки Python
    - HTML будет поступать через stdin
    - печатай данные через `print` в человеко-читаемом виде
    - извлекай информацию из всех частей страницы

    HTML:
    ```html
    {html_content}
    ```
    """

    response = client.chat.complete(
        model="mistral-large-latest",
        messages=[{"role": "system", "content": system_prompt},{"role": "user", "content": prompt}]
    )

    raw_output=response.choices[0].message.content
    match = re.search(r"```python(.*?)```", raw_output, re.DOTALL)
    if match:
        return match.group(1).strip()
    else:
        raise ValueError("Не удалось найти Python-код в ответе модели.")


# --- Этап 3: Выполнение сгенерированного парсера ---
def execute_parser(parser_code, html_content):
    try:
        # Создаем временный файл с парсером
        with open("temp_parser.py", "w", encoding='utf-8') as f:
            f.write(parser_code)

        # Выполняем парсер и получаем результат
        result = subprocess.run(
            [sys.executable, "temp_parser.py"],
            input=html_content,
            capture_output=True,
            text=True,
            encoding='utf-8'
        )

        return result.stdout
    finally:
        import os
        os.remove("temp_parser.py")


# --- Основной workflow ---
def parse(url,api_key):
    # 1. Получаем HTML
    html = get_rendered_html(url)
    cleaned_html = clean_html_for_llm(html)
    print(cleaned_html)

    parser_code = generate_parser(cleaned_html, api_key)

    print("===== GENERATED PARSER =====")
    print(parser_code)
    print("===== END PARSER =====")

    # 3. Выполняем парсер
    return execute_parser(parser_code, html)


api_key = "api_key"
model = "mistral-large-latest"
url = "https://www.gismeteo.ru/weather-sankt-peterburg-4079/"
print(parse(url, api_key))