from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait

def get_rendered_html(url, timeout=10):
    # Настройки для headless-режима (без открытия окна браузера)
    options = Options()
    options.add_argument("--headless")             # Без окна браузера
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--window-size=1920,1080")

    # Запуск браузера
    driver = webdriver.Chrome(options=options)

    try:
        driver.get(url)

        # Явное ожидание загрузки содержимого (можно уточнить по CSS/XPath)
        WebDriverWait(driver, timeout).until(
            lambda d: d.execute_script("return document.readyState") == "complete"
        )

        # Получаем финальный HTML (всё, как его видит пользователь)
        rendered_html = driver.page_source
        return rendered_html

    finally:
        driver.quit()

url = "https://www.gismeteo.ru/weather-sankt-peterburg-4079/"
# url="https://vc.ru/ai/1741336-kak-skompilirovat-soderzhimoe-veb-saita-dlya-izucheniya-llms"
# url="https://education.yandex.ru/handbook/ml"
html = get_rendered_html(url)
print(html)



from bs4 import BeautifulSoup

def extract_clean_text(html_content: str) -> str:
    soup = BeautifulSoup(html_content, 'html.parser')
    # Удаление скриптов, стилей, noscript
    for tag in soup(["script", "style", "noscript"]):
        tag.decompose()
    # Возможная дополнительная очистка: можно добавить эвристику по удалению рекламных блоков по классам/идентификаторам
    text = soup.get_text(separator='\n')
    # Очистка: удаление пустых строк и лишних пробелов
    lines = [line.strip() for line in text.splitlines() if line.strip()]
    return "\n".join(lines)

# Пример использования:
clean_text = extract_clean_text(html)
# print(clean_text)



# import requests
#
# url="https://www.gismeteo.ru/weather-sankt-peterburg-4079/"
# headers = {
#     "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36",
#     "Accept-Language": "ru-RU,ru;q=0.9,en;q=0.8",
# }
#
# html_content = requests.get(url, headers=headers)
# print(html_content.status_code)
# print(html_content.text)



meta_data="Город, Температура сейчас"



from mistralai import Mistral
# api_key = os.environ["MISTRAL_API_KEY"]
api_key = "api_key"
model = "mistral-large-latest"
# model = "pixtral-12b-2409"

client = Mistral(api_key=api_key)

system_prompt = (
    """"Ты языковая модель, выполняющая *исключительно* структурирование и очистку текста,
    без добавления новых фраз, переиначивания смыслов или выдумывания информации.
    Твоя задача — убрать HTML-артефакты, дубли, повторяющиеся блоки, рекламные вставки и прочий шум,
    оставив только чистую, читаемую, максимально близкую к оригиналу версию текста.
    Так же, после обработки текста извлеки и сохрани метаданные, которые переданы пользователем.
    Ответ должен быть строго в формате JSON со следующими ключами:
    {
    "cleaned_text": "<очищенный текст здесь>"
    "meta_data": "<мета данные, которые запросил пользователь>"
    }
    """
)


chat_response = client.chat.complete(
    model = model,
    messages = [
        {"role": "system", "content": system_prompt},
        {
            "role": "user",
            "content": f"""
                Ниже приведён текст, извлечённый с веб-страницы.
                Он может содержать остаточные HTML-теги, рекламные вставки и неидеальное форматирование.
                Очисти и структурируй текст, убери все HTML-артефакты и сделай его читаемым.
                Верни результат строго в формате JSON:
                {{
                "cleaned_text": "<очищенный текст здесь>"
                "meta_data": "<мета данные, которые запросил пользователь>"
                }}
                Вот мета-данные, которые следует извлечь из текста: {meta_data},
                Вот текст: {clean_text}
            """

        },
    ],
    temperature=0.2,
)

print(chat_response.choices[0].message.content)

import json

response_text = chat_response.choices[0].message.content

def clean_json_string(raw_json: str) -> str:
    """
    Удаляет обёртку ```json и ```
    """
    lines = raw_json.strip().splitlines()
    lines = [line for line in lines if not line.strip().startswith("```")]
    return "\n".join(lines)

def save_clean_json(raw_json: str, filename: str):
    cleaned = clean_json_string(raw_json)
    try:
        data = json.loads(cleaned)
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        print(f"Файл успешно сохранён: {filename}")
    except json.JSONDecodeError as e:
        print(f"Ошибка при разборе JSON: {e}")

save_clean_json(response_text, "output.json")

# # Страховка от неожиданных символов
# response_text = response_text.replace('“', '"').replace('”', '"')
# response_text = response_text.replace('’', "'").replace('‘', "'")
# response_text = re.sub(r'[–—]', '-', response_text)  # длинные тире → обычное