import os
from typing import List, Optional, Any, Dict

from autoparse.dispatcher import get_pipeline
from autoparse.tools.fetchers.static_fetcher import fetch_static_html
from autoparse.tools.fetchers.dynamic_fetcher import fetch_dynamic_html
from autoparse.cache.code_cache import ParserCodeCache
from autoparse.tools.llm.client import LLMClient
from autoparse.tools.converter.converterRunParser import run_and_convert_parser
from autoparse.tools.fetchers.dynamic_detector import is_dynamic_site

class Parser:
    """
    Main entry point for parsing a URL.

    Supports two modes:
      - structuring: full clean + LLM structuring → JSON with cleaned_text & meta_data
      - codegen: light clean + LLM codegen → return parser code (cached by URL)
      - auto: picks structuring for dynamic sites, codegen otherwise
    """

    def __init__(
        self,
        cache_dir: str = None,
        api_key: str = None,
        model: str = None
    ):
        # LLM client (Mistral)
        self.client = LLMClient(api_key=api_key, model=model)

        # set up code cache for codegen mode
        base = cache_dir or os.getenv(
            "CACHE_DIR",
            os.path.join("autoparse", "cache")
        )
        self.code_cache = ParserCodeCache(base)


    def parse_url(
        self,
        url: str,
        meta: Optional[List[str]],
        user_query: str,
        mode: str = "auto",
        dynamic: bool = None,
        timeout: int = 10,
        regenerate: bool = False
    ) -> Dict[str, Any]:
        """
        Fetch, clean and parse a URL.

        Args:
            url: target URL
            meta: metadata fields for structuring mode
            mode: "auto" | "structuring" | "codegen"
            dynamic: if True, render JS with Selenium
            timeout: fetch timeout in seconds

        Returns:
            - structuring → dict with "cleaned_text" and "meta_data"
            - codegen     → dict with "parser_code"
        """
        should_render = is_dynamic_site(url, timeout=timeout)
        # 1) fetch HTML (static or dynamic)
        if should_render:
            html = fetch_dynamic_html(url, timeout=timeout)
        else:
            html = fetch_static_html(url, timeout=timeout)

        if mode == "codegen" and regenerate:
            # сначала пробуем точное совпадение
            deleted = self.code_cache.delete(url, user_query, semantic=False)
            if not deleted:
                # иначе — любое семантическое совпадение
                self.code_cache.delete(url, user_query, semantic=True)

        # 2) pick cleaning & parsing strategies
        cleaning_strategy, parsing_strategy = get_pipeline(html, mode, self.code_cache)

        # 3) clean HTML
        cleaned_html = cleaning_strategy.clean(html)

        result = parsing_strategy.parse(
            cleaned_html,
            meta,
            self.client,
            url=url,
            user_query=user_query
        )

        if mode == "codegen":
            return run_and_convert_parser(
                result["parser_code"],
                cleaned_html
            )

        return result





