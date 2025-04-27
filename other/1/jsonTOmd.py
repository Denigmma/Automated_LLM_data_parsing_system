import json


def json_to_markdown(data, level=1):
    """Рекурсивно конвертирует JSON в Markdown"""
    markdown = ""

    if isinstance(data, dict):
        for key, value in data.items():
            markdown += f"{'#' * level} {key}\n\n"
            markdown += json_to_markdown(value, level + 1)
    elif isinstance(data, list):
        for item in data:
            markdown += f"{json_to_markdown(item, level)}\n"
    else:
        markdown += f"{data}\n\n"

    return markdown


# Читаем JSON-файл
with open('output.json', 'r', encoding='utf-8') as file:
    json_data = json.load(file)

# Конвертируем в Markdown
markdown_output = json_to_markdown(json_data)

# Сохраняем в .md файл
with open('output.md', 'w', encoding='utf-8') as md_file:
    md_file.write(markdown_output)

print("✅ Универсальный Markdown файл успешно создан!")
