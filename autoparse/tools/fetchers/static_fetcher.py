import requests
from typing import Optional

def fetch_static_html(
    url: str,
    timeout: int = 10,
    headers: Optional[dict] = None
) -> str:
    """
    Fetch HTML from a static site via HTTP GET.

    Args:
        url: target URL
        timeout: request timeout in seconds
        headers: optional dict of HTTP headers to send

    Returns:
        raw HTML as a string

    Raises:
        requests.HTTPError on bad HTTP status
        requests.RequestException on network errors
    """
    default_headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/115.0.0.0 Safari/537.36"
        ),
        "Accept-Language": "en-US,en;q=0.9"
    }
    # merge headers
    hdrs = default_headers.copy()
    if headers:
        hdrs.update(headers)

    resp = requests.get(url, headers=hdrs, timeout=timeout)
    resp.raise_for_status()
    return resp.text
