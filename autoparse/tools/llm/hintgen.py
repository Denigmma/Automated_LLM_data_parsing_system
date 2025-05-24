from .client import LLMClient
from .prompts import SYSTEM_PROMPT_HINTGEN, USER_PROMPT_HINT_TEMPLATE


def generate_parsing_hints(html: str, user_query: str, client: LLMClient) -> str:
    """
    Первый LLM-запрос: анализ HTML + юзер-запроса, выдача подсказок
    (селекторы, блоки, формат вывода) для последующего Codegen.
    """
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT_HINTGEN},
        {"role": "user", "content": USER_PROMPT_HINT_TEMPLATE.format(
            html=html,
            query=user_query
        )},
    ]
    response = client.chat_complete(messages=messages)
    print(response.choices[0].message.content.strip())
    return response.choices[0].message.content.strip()
