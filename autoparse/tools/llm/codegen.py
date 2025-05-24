import re
from typing import Optional

from .client import LLMClient
from .prompts import SYSTEM_PROMPT_CODEGEN, USER_PROMPT_CODEGEN_TEMPLATE


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
