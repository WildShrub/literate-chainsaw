"""
Union type narrowing errors - LLMs often miss these subtle type issues.
mypy will catch that we're not properly narrowing union types.
"""
from typing import Union, List

def process_value(val: Union[int, str, None]) -> str:
    """Process a value that could be int, str, or None."""
    # LLM might miss: if val is not None doesn't narrow to int|str properly
    if val is not None:
        # mypy knows val could still be int or str here
        return val.split(',')[0]  # ERROR: int has no split method


def get_first_element(data: Union[List[int], dict]) -> int:
    """Get first element from a list or dict."""
    if isinstance(data, list):
        # mypy knows data is List[int] here
        return data[0]
    else:
        # mypy knows data is dict here
        return data['key']  # ERROR: dict[Any, Any] returns Any, not int


def handle_union(value: Union[int, str]) -> int:
    """Handle a union type."""
    if value:  # Truthiness check doesn't narrow the type!
        # mypy sees value is still Union[int, str] - could be empty str or 0
        return int(value) + 10
    return 0


def risky_access(item: Union[str, None]) -> int:
    """Access attributes on union."""
    # LLM might think the or handles it, but mypy catches the real issue
    text = item or ""
    # mypy knows text is str here
    return text.count('x')  # This is fine
