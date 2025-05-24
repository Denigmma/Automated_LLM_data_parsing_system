import os
from mistralai import Mistral
import tiktoken

MAX_INPUT_TOKENS = int(os.getenv("MAX_INPUT_TOKENS"))


class LLMClient:
    """
    Simple wrapper around the Mistral API.
    """

    def __init__(self, api_key: str = None, model: str = None):
        # You can pass api_key explicitly or set MISTRAL_API_KEY in env
        self.api_key = api_key or os.getenv("MISTRAL_API_KEY")
        if not self.api_key:
            raise ValueError("LLM API key must be provided via parameter or MISTRAL_API_KEY env var.")
        # Default model, can override via env LLM_MODEL
        self.model = model or os.getenv("LLM_MODEL")
        self.client = Mistral(api_key=self.api_key)

    def chat_complete(self, messages: list[dict], temperature: float = None):
        """
        Send a chat completion request to the LLM.
        """
        truncated_messages = []
        for msg in messages:
            role = msg.get("role")
            content = msg.get("content", "")
            if role in ("system", "user"):
                content = truncate_to_max_tokens(content, self.model)
            truncated_messages.append({"role": role, "content": content})

        return self.client.chat.complete(
            model=self.model,
            messages=messages,
            temperature=temperature,
        )


def truncate_to_max_tokens(text: str, model_name: str, max_tokens: int = MAX_INPUT_TOKENS) -> str:
    """
    Обрезает текст до max_tokens токенов по кодировщику tiktoken для указанной модели.
    """
    try:
        encoding = tiktoken.encoding_for_model(model_name)
    except Exception:
        encoding = tiktoken.get_encoding("cl100k_base")
    token_ids = encoding.encode(text)
    if len(token_ids) > max_tokens:
        token_ids = token_ids[-max_tokens:]
    return encoding.decode(token_ids)