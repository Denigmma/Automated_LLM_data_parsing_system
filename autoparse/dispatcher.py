from autoparse.strategies.cleaning import FullCleaningStrategy, LightCleaningStrategy
from autoparse.strategies.parsing import StructuringParsingStrategy, CodegenParsingStrategy


def is_dynamic_site(html: str) -> bool:
    """
    Heuristic to detect if a site is dynamically rendered (i.e. needs JS).
    """
    return "window.__INITIAL_STATE__" in html or "<div id=\"root\"" in html


def get_pipeline(html: str, mode: str = "auto"):
    """
    Choose cleaning and parsing strategies.

    Args:
        html: raw HTML of the page
        mode: one of
          - "auto": detect based on html
          - "structuring": always do full clean + LLM→JSON
          - "codegen": always do light clean + LLM→codegen

    Returns:
        (cleaning_strategy, parsing_strategy)
    """
    if mode == "structuring":
        return FullCleaningStrategy(), StructuringParsingStrategy()
    if mode == "codegen":
        return LightCleaningStrategy(), CodegenParsingStrategy()

    # auto mode
    if is_dynamic_site(html):
        return FullCleaningStrategy(), StructuringParsingStrategy()
    else:
        return LightCleaningStrategy(), CodegenParsingStrategy()