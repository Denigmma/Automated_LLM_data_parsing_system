import os
from mistralai import Mistral

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

        return self.client.chat.complete(
            model=self.model,
            messages=messages,
            temperature=temperature,
        )

