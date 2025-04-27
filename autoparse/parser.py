import os
from typing import Any, Dict

from autoparse.dispatcher import get_pipeline
from autoparse.tools.fetchers.static_fetcher import fetch_static_html
from autoparse.tools.fetchers.dynamic_fetcher import fetch_dynamic_html
from autoparse.cache.code_cache import ParserCodeCache
from autoparse.tools.llm.client import LLMClient
from autoparse.tools.llm.structuring import parse_structured
from autoparse.tools.llm.codegen import generate_parser
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
        meta: Dict[str, Any],
        mode: str = "auto",
        dynamic: bool = None,
        timeout: int = 10
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

        # 2) pick cleaning & parsing strategies
        cleaning_strategy, parsing_strategy = get_pipeline(html, mode)

        # 3) clean HTML
        cleaned_html = cleaning_strategy.clean(html)

        # 4) branch by mode
        if mode == "codegen":
            # try cache first
            code = self.code_cache.get(url)
            if code is None:
                # generate new parser code
                code = generate_parser(cleaned_html, self.client)
                self.code_cache.store(url, code)
            result = run_and_convert_parser(code, cleaned_html)
            return result

        # structuring (includes auto→structuring for dynamic)
        return parse_structured(cleaned_html, meta, self.client)