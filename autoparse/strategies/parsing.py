from abc import ABC, abstractmethod
from typing import Any, Dict, List
import os

from autoparse.tools.llm.client import LLMClient
from autoparse.tools.llm.structuring import parse_structured
from autoparse.tools.llm.hintgen import generate_parsing_hints
from autoparse.tools.llm.codegen import generate_parser
from autoparse.cache.code_cache import ParserCodeCache


class ParsingStrategy(ABC):
    """
    Abstract base for parsing strategies.
    """
    @abstractmethod
    def parse(
        self,
        cleaned: str,
        meta: Dict[str, Any],
        client: LLMClient,
        **kwargs
    ) -> Dict[str, Any]:
        """
        Given cleaned HTML/text, produce the final result.
        """
        pass


class StructuringParsingStrategy(ParsingStrategy):
    def parse(
        self,
        cleaned: str,
        meta: List[str],
        client: LLMClient,
        **kwargs
    ) -> Dict[str, Any]:
        return parse_structured(cleaned, meta, client, kwargs["user_query"])



class CodegenParsingStrategy(ParsingStrategy):
    """
    Strategy #2: code-generation with semantic cache.
    """
    def __init__(self, code_cache: ParserCodeCache):
        self.code_cache = code_cache


    def parse(
        self,
        cleaned: str,
        meta: Dict[str, Any],
        client: LLMClient,
        **kwargs
    ) -> Dict[str, Any]:
        """
        kwargs должно содержать:
          - url: str
          - user_query: str
        """
        url = kwargs["url"]
        user_query = kwargs["user_query"]

        # семантический поиск в ChromaDB
        hit = self.code_cache.find_similar(url, user_query)
        if hit:
            file_path = hit["file_path"]
            full_path = os.path.join(self.code_cache.code_dir, file_path)
            with open(full_path, "r", encoding="utf-8") as f:
                code = f.read()
        else:
            try:
                hints = generate_parsing_hints(cleaned, user_query, client)
            except Exception:
                hints = None
            code = generate_parser(cleaned, user_query, client, hint=hints)
            self.code_cache.store(url, user_query, code)

        return {"parser_code": code}