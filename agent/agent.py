# agent/agent.py

from typing import Any, Dict, List, Optional
from agent.tools_mapping import parse_url as _parse_url

def run_agent(
    url: str,
    meta: Optional[List[str]] = None,
    mode: str = "auto",
    dynamic: Optional[bool] = None,
    timeout: int = 10
) -> Dict[str, Any]:
    """
    Main entrypoint for your “agent” façade.

    Just delegates to agent.tools_mapping.parse_url.
    """
    return _parse_url(
        url     = url,
        meta    = meta or [],
        mode    = mode,
        dynamic = dynamic,
        timeout = timeout
    )
