from abc import ABC, abstractmethod
from autoparse.tools.cleaners.full_cleaner import extract_full_clean_text
from autoparse.tools.cleaners.partial_cleaner import extract_partial_clean_html


class CleaningStrategy(ABC):
    """
    Abstract base for HTML cleaning strategies.
    """
    @abstractmethod
    def clean(self, html: str) -> str:
        """
        Clean the raw HTML and return either plain text or a reduced HTML.
        """
        pass


class FullCleaningStrategy(CleaningStrategy):
    """
    Full‐clean strategy: drop all HTML and return only plain text.
    """
    def clean(self, html: str) -> str:
        return extract_full_clean_text(html)


class LightCleaningStrategy(CleaningStrategy):
    """
    Partial‐clean strategy: shrink the HTML but preserve structure
    for code‐generation parsers.
    """
    def clean(self, html: str) -> str:
        return extract_partial_clean_html(html)
