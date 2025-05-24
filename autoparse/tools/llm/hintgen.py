from .client import LLMClient
from .prompts import SYSTEM_PROMPT_HINTGEN, USER_PROMPT_HINT_TEMPLATE, token_message_error
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


def generate_parsing_hints(html: str, user_query: str, client: LLMClient) -> str:
    """
    Первый LLM-запрос: анализ HTML + юзер-запроса, выдача подсказок
    (селекторы, блоки, формат вывода) для последующего Codegen.
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
        {"role": "system", "content": SYSTEM_PROMPT_HINTGEN},
        {"role": "user", "content": USER_PROMPT_HINT_TEMPLATE.format(
            html=html,
            query=user_query
        )},
    ]
    response = client.chat_complete(messages=messages)
    print(response.choices[0].message.content.strip())
    return response.choices[0].message.content.strip()
