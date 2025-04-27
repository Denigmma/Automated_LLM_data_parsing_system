from typing import Any, Dict, List, Union

def json_to_text(
    data: Union[Dict[str, Any], List[Any], Any],
    indent: int = 0
) -> str:
    """
    Рекурсивно обходит JSON-структуру и превращает её
    в человекочитаемый многострочный текст.
    """
    lines: List[str] = []
    prefix = ' ' * indent

    if isinstance(data, dict):
        for key, value in data.items():
            if isinstance(value, (dict, list)):
                lines.append(f"{prefix}{key}:")
                lines.append(json_to_text(value, indent + 2))
            else:
                lines.append(f"{prefix}{key}: {value}")
    elif isinstance(data, list):
        for item in data:
            if isinstance(item, (dict, list)):
                lines.append(f"{prefix}-")
                lines.append(json_to_text(item, indent + 2))
            else:
                lines.append(f"{prefix}- {item}")
    else:
        # простое значение
        lines.append(f"{prefix}{data}")

    return "\n".join(lines)
