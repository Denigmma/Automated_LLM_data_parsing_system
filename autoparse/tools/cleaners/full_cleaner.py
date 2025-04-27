from bs4 import BeautifulSoup, Comment
from typing import List


def extract_full_clean_text(html: str) -> str:
    """
    Fully cleans HTML content and returns only readable text.

    Removes:
      - <script>, <style>, <noscript> and other non‐text tags
      - <head>, <meta>, <link>, <svg>
      - HTML comments
      - advertisement/utility blocks by common CSS classes
      - empty tags (without text or media)

    Returns:
      A multi-line string where each non-empty line corresponds to
      a piece of content from the original HTML.
    """
    soup = BeautifulSoup(html, 'html.parser')

    for tag in soup.find_all([
        'script', 'style', 'noscript',
        'head', 'meta', 'link', 'svg'
    ]):
        tag.decompose()
    for comment in soup.find_all(string=lambda text: isinstance(text, Comment)):
        comment.extract()

    blacklist_classes: List[str] = [
        "header", "footer", "nav", "navbar", "breadcrumbs", "sidebar",
        "adfox", "media-top", "media-right", "media-bottom", "advert",
        "subscription", "cookie", "popup", "banner", "tracker", "metrika",
        "header__bottom", "header__top", "footer__inner", "footer__menu"
    ]
    for cls in blacklist_classes:
        for tag in soup.select(f".{cls}"):
            tag.decompose()

    for tag in soup.find_all():
        if not tag.get_text(strip=True) and not tag.find(['img', 'iframe']):
            tag.decompose()

    raw_text = soup.get_text(separator="\n")
    lines = [line.strip() for line in raw_text.splitlines() if line.strip()]

    return "\n".join(lines)