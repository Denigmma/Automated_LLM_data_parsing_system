import json
import re
from typing import Dict, Any
from .client import LLMClient
from .prompts import SYSTEM_PROMPT_STRUCTURING, USER_PROMPT_STRUCTURING_TEMPLATE

from typing import List

def parse_structured(
    html: str,
    meta: List[str],
    client: LLMClient,
    user_query: str
) -> Dict[str, Any]:

    messages = [
        {"role": "system", "content": SYSTEM_PROMPT_STRUCTURING},
        {"role": "user", "content": USER_PROMPT_STRUCTURING_TEMPLATE.format(
            html=html,
            meta=meta,
            user_query=user_query
        )}
    ]
    resp = client.chat_complete(messages, temperature=0.2)
    raw = resp.choices[0].message.content.strip()

    m = re.search(r"```(?:json)?\s*([\s\S]*?)```", raw, re.IGNORECASE)
    if m:
        body = m.group(1).strip()
    else:
        m2 = re.search(r"\{[\s\S]*\}", raw)
        if m2:
            body = m2.group(0)
        else:
            raise ValueError(f"Не удалось извлечь JSON из ответа LLM:\n{raw}")

    try:
        return json.loads(body)
    except json.JSONDecodeError as e:
        raise ValueError(f"Ошибка JSON-разбора: {e}\nТекст для разбора:\n{body}")