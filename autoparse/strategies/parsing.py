from abc import ABC, abstractmethod
from typing import Any, Dict

from autoparse.tools.llm.client import LLMClient
from autoparse.tools.llm.structuring import parse_structured
from autoparse.tools.llm.codegen import generate_parser


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
    """
    Strategy #1: plain-text structuring.
    Uses LLM to produce JSON with cleaned_text + meta_data.
    """
    def parse(
        self,
        cleaned: str,
        meta: Dict[str, Any],
        client: LLMClient,
        **kwargs
    ) -> Dict[str, Any]:
        # parse_structured returns a dict with keys "cleaned_text" and "meta_data"
        return parse_structured(cleaned, meta, client)


class CodegenParsingStrategy(ParsingStrategy):
    """
    Strategy #2: code-generation.
    Uses LLM to generate a Python parser script and returns it.
    """
    def parse(
        self,
        cleaned: str,
        meta: Dict[str, Any],
        client: LLMClient,
        **kwargs
    ) -> Dict[str, Any]:
        # url will be used downstream by parser cache
        parser_code = generate_parser(cleaned, client)
        return {"parser_code": parser_code}
