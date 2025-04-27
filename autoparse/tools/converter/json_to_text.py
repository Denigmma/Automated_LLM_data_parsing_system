from typing import Any, Dict, List, Union

def convert_json_to_text(data: Union[Dict[str, Any], List[Any]]) -> str:
    """
    Recursively walk the JSON-like dict/list and produce
    a nicely indented text representation.
    """
    lines: List[str] = []

    def _render(obj: Any, indent: int = 0):
        prefix = "  " * indent
        if isinstance(obj, dict):
            for key, val in obj.items():
                if isinstance(val, (dict, list)):
                    lines.append(f"{prefix}{key}:")
                    _render(val, indent + 1)
                else:
                    lines.append(f"{prefix}{key}: {val}")
        elif isinstance(obj, list):
            for item in obj:
                if isinstance(item, (dict, list)):
                    lines.append(f"{prefix}-")
                    _render(item, indent + 1)
                else:
                    lines.append(f"{prefix}- {item}")
        else:
            # primitive
            lines.append(f"{prefix}{obj}")

    _render(data, indent=0)
    return "\n".join(lines)
