import json
import re
from typing import Dict, Any
from .client import LLMClient
from .prompts import SYSTEM_PROMPT_STRUCTURING, USER_PROMPT_STRUCTURING_TEMPLATE, token_message_error
from typing import List

import os
import tiktoken
MAX_INPUT_TOKENS = int(os.getenv("MAX_INPUT_TOKENS"))

model_name = os.getenv("LLM_MODEL")

try:
    tokenizer = tiktoken.encoding_for_model(model_name)
except KeyError:
    tokenizer = tiktoken.get_encoding("cl100k_base")

def num_tokens(text: str) -> int:
    return len(tokenizer.encode(text))

def parse_structured(
    html: str,
    meta: List[str],
    client: LLMClient,
    user_query: str
) -> Dict[str, Any]:

    uq_toks = num_tokens(user_query)
    err_toks = num_tokens(token_message_error)

    if num_tokens(html) + uq_toks > MAX_INPUT_TOKENS:
        available_for_html = MAX_INPUT_TOKENS - uq_toks - err_toks
        if available_for_html < 0:
            available_for_html = 0

        html_toks = tokenizer.encode(html)
        truncated_html_toks = html_toks[:available_for_html]
        html = tokenizer.decode(truncated_html_toks) + token_message_error


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