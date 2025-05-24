from typing import Any, Dict, List, Optional
from agent.tools_mapping import parse_url as _parse_url


def run_agent(
        url: str,
        user_query: str,
        meta: Optional[List[str]] = None,
        mode: str = "auto",
        dynamic: Optional[bool] = None,
        timeout: int = 10,
        regenerate: bool = False
) -> Dict[str, Any]:
    """
    Main entrypoint for your “agent” façade.

    Args:
      url:        страница для парсинга
      user_query: текст запроса пользователя, чтобы извлекать только нужные данные
      meta:       для режима 'structuring', список полей метаданных
      mode:       'auto' | 'structuring' | 'codegen'
      dynamic:    True → использовать Selenium
      timeout:    таймаут в секундах

    Делегирует к agent.tools_mapping.parse_url.
    """
    return _parse_url(
        url=url,
        user_query=user_query,
        meta=meta or [],
        mode=mode,
        dynamic=dynamic,
        timeout=timeout,
        regenerate=regenerate
    )
