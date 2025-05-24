import os
from typing import Any, Dict, List, Optional

from autoparse.parser import Parser

# we keep a single Parser instance, but initialize lazily
_parser_instance: Optional[Parser] = None


def _get_parser() -> Parser:
    global _parser_instance
    if _parser_instance is None:
        # read from env or defaults
        api_key = os.getenv("MISTRAL_API_KEY")
        model = os.getenv("LLM_MODEL", None)
        cache_dir = os.getenv("CACHE_DIR", None)
        _parser_instance = Parser(
            cache_dir=cache_dir,
            api_key=api_key,
            model=model
        )
    return _parser_instance


def parse_url(
    url: str,
    user_query: str,
    meta: Optional[List[str]] = None,
    mode: str = "auto",
    dynamic: bool = False,
    timeout: int = 10,
    regenerate: bool = False
) -> Dict[str, Any]:
    """
    High-level façade over autoparse.Parser.parse_url.

    Args:
      url:        страница для парсинга
      user_query: текст запроса пользователя
      meta:       список полей метаданных (для structuring)
      mode:       'auto' | 'structuring' | 'codegen'
      dynamic:    True → использовать Selenium
      timeout:    таймаут в секундах
    """
    parser = _get_parser()
    return parser.parse_url(
        url=url,
        meta=meta or [],
        user_query=user_query,
        mode=mode,
        dynamic=dynamic,
        timeout=timeout,
        regenerate=regenerate
    )
