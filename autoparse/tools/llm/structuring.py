import json
import re
from .client import LLMClient
from .prompts import SYSTEM_PROMPT_STRUCTURING, USER_PROMPT_STRUCTURING_TEMPLATE

def parse_structured(text: str, meta: dict, client: LLMClient) -> dict:
    # Подготавливаем содержимое prompt'а
    user_content = USER_PROMPT_STRUCTURING_TEMPLATE.format(
        meta_data=json.dumps(meta, ensure_ascii=False),
        clean_text=text
    )

    messages = [
        {"role": "system", "content": SYSTEM_PROMPT_STRUCTURING},
        {"role": "user",   "content": user_content}
    ]
    resp = client.chat_complete(messages, temperature=0.2)
    raw = resp.choices[0].message.content.strip()

    # 3) Пытаемся вытащить блок между ```json ... ```
    m = re.search(r"```(?:json)?\s*([\s\S]*?)```", raw, re.IGNORECASE)
    if m:
        body = m.group(1).strip()
    else:
        # 4) Иначе — ищем первый {...} в любом месте
        m2 = re.search(r"\{[\s\S]*\}", raw)
        if m2:
            body = m2.group(0)
        else:
            # Ничего не нашли — кидаем понятную ошибку
            raise ValueError(f"Не удалось извлечь JSON из ответа LLM:\n{raw}")

    # 5) Парсим JSON
    try:
        return json.loads(body)
    except json.JSONDecodeError as e:
        raise ValueError(f"Ошибка JSON-разбора: {e}\nТекст для разбора:\n{body}")