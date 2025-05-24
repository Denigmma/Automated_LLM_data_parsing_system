import re
from typing import Optional

from .client import LLMClient
from .prompts import SYSTEM_PROMPT_CODEGEN, USER_PROMPT_CODEGEN_TEMPLATE, token_message_error

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


def generate_parser(
        html: str,
        user_query: str,
        client: LLMClient,
        hint: Optional[str] = None
) -> str:
    """
    Invoke the LLM to generate a Python parser for the given HTML,
    extracting **only** data requested in user_query.
    Returns the raw Python code (without markdown fences).
    """

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
        {"role": "system", "content": SYSTEM_PROMPT_CODEGEN},
        {"role": "user", "content": USER_PROMPT_CODEGEN_TEMPLATE.format(
            query=user_query,
            hint=hint or "",
            html=html
        )},
    ]
    response = client.chat_complete(messages, temperature=None)
    raw = response.choices[0].message.content

    match = re.search(r"```python(.*?)```", raw, re.DOTALL)
    if match:
        return match.group(1).strip()
    raise ValueError("No Python code block found in LLM response")
