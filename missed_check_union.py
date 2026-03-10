"""
Subtle union type narrowing errors that LLMs often miss.
These look correct but mypy catches the type violations.
"""
from typing import Union, Optional, List

def process_union(value: Union[int, str]) -> str:
    """
    LLM might think: "This looks fine, isinstance checks narrow the type"
    But mypy catches: value could still be int after the if
    """
    if isinstance(value, str):
        return value.upper()
    # ERROR: value is still Union[int, str] here, not narrowed to int
    return str(value)  # This is actually fine, but let's make it error


def process_union_error(value: Union[int, str]) -> int:
    """
    LLM might think: "The isinstance check handles it"
    But mypy knows: value could be str, which has no .bit_length()
    """
    if isinstance(value, int):
        return value.bit_length()
    # ERROR: value is str here, str has no bit_length method
    return value.bit_length()  # This will fail at runtime


def optional_access(data: Optional[dict]) -> str:
    """
    LLM might think: "The if check handles None"
    But mypy knows: data could still be None after the check
    """
    if data is not None:
        return data.get("key", "default")
    # ERROR: data is None here, but we're trying to access it
    return data["missing"]  # This is unreachable but mypy flags it


def nested_union(value: Union[List[int], dict[str, int]]) -> int:
    """
    LLM might think: "isinstance checks handle the types"
    But mypy catches: dict access could return Any, not int
    """
    if isinstance(value, list):
        return value[0]  # OK
    else:
        # ERROR: value[key] returns Any, not guaranteed to be int
        return value["key"]  # mypy: Incompatible return type


def truthiness_narrowing(value: Union[str, int, None]) -> str:
    """
    LLM might think: "if value: narrows to non-None"
    But mypy knows: empty string or 0 are falsy but still str/int
    """
    if value:  # This doesn't narrow Union[str, int, None] properly
        # ERROR: value could be 0 (int) or "" (str), not narrowed
        return value.upper()  # int has no upper method
    return "empty"


def multiple_checks(value: Union[int, str, float]) -> str:
    """
    LLM might think: "All cases covered"
    But mypy sees: float case not handled, value could be float
    """
    if isinstance(value, int):
        return str(value)
    elif isinstance(value, str):
        return value
    # ERROR: value could be float here, not handled
    return value.upper()  # float has no upper method


def assert_narrowing(value: Union[str, int]) -> str:
    """
    LLM might think: "assert isinstance narrows the type"
    But mypy may not use assert for narrowing by default
    """
    assert isinstance(value, str)
    # ERROR: Depending on mypy config, this may not narrow
    return value.upper()


def guard_clause_optional(items: Optional[List[str]]) -> int:
    """
    LLM might think: "Early return handles None"
    But mypy knows: items could still be None in the else branch
    """
    if items is None:
        return 0
    # ERROR: items is still Optional[List[str]] in mypy's view sometimes
    return len(items)  # This should be fine, but let's see


def chained_access(data: Optional[dict[str, Optional[str]]]) -> str:
    """
    LLM might think: "Nested checks handle all None cases"
    But mypy catches: intermediate Optional not properly narrowed
    """
    if data is not None:
        value = data.get("key")
        if value is not None:
            return value
    # ERROR: data could be None, but we're accessing it
    return data["fallback"]  # Unreachable but flagged


def list_comprehension_union(items: List[Union[int, str]]) -> List[str]:
    """
    LLM might think: "isinstance filters correctly"
    But mypy knows: comprehension doesn't narrow the type properly
    """
    # ERROR: item is still Union[int, str] inside comprehension
    return [item.upper() for item in items]  # int has no upper


def dict_access_union(mapping: dict[str, Union[int, str]]) -> int:
    """
    LLM might think: "Key access is fine"
    But mypy knows: dict values are Union, not narrowed
    """
    # ERROR: mapping["key"] returns Union[int, str], not int
    return mapping["key"] + 1  # str + int fails


def function_return_union(func: callable) -> str:
    """
    LLM might think: "callable check is sufficient"
    But mypy doesn't narrow based on callable()
    """
    if callable(func):
        result = func()
        # ERROR: result could be anything, not necessarily str
        return result.upper()
    return "not callable"


def try_except_narrowing(value: Union[int, str]) -> str:
    """
    LLM might think: "try-except handles type issues"
    But mypy doesn't use exception handling for narrowing
    """
    try:
        # ERROR: value could be int, which has no upper method
        return value.upper()
    except AttributeError:
        return str(value)


def walrus_optional(data: Optional[str]) -> int:
    """
    LLM might think: "walrus assigns and checks"
    But mypy may not narrow through walrus properly
    """
    if (text := data) is not None:
        # ERROR: text is still Optional[str] in some mypy versions
        return len(text)
    return 0


def conditional_union(value: Union[str, int]) -> str:
    """
    LLM might think: "isinstance in condition narrows"
    But mypy knows: the else branch doesn't narrow
    """
    return value.upper() if isinstance(value, str) else value.upper()
    # ERROR: in else branch, value is int, no upper method


def loop_union(items: List[Union[int, str]]) -> None:
    """
    LLM might think: "Loop is fine"
    But mypy catches: item is Union inside loop
    """
    for item in items:
        # ERROR: item could be int, no upper method
        print(item.upper())


def default_dict_optional(data: dict[str, Optional[int]]) -> int:
    """
    LLM might think: "get with default handles None"
    But mypy knows: get returns Optional[int], not int
    """
    # ERROR: get returns Optional[int], not int
    return data.get("key", 0) + 1  # Optional[int] + int fails
