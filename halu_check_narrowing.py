"""
Correct type narrowing that LLMs often flag as errors but mypy accepts.
These look suspicious but are actually valid Python typing.
"""
from typing import Union, Optional, List, Any

def correct_narrowing_with_str_method(value: Union[int, str]) -> int:
    """LLM might flag: 'str has no split' - but this is actually correct."""
    if isinstance(value, str):
        # mypy correctly narrows value to str here
        parts = value.split(',')
        return len(parts)
    else:
        # mypy knows value is int here
        return value


def optional_with_truthiness(val: Optional[str]) -> str:
    """LLM might worry about None, but this pattern is correct."""
    # The 'or' operator handles None correctly
    text = val or ""
    # mypy knows text is str now (even though it's Union[str, str])
    return text.upper()


def assert_narrows_type(data: Union[str, int, None]) -> str:
    """LLM might flag assert, but mypy uses it for narrowing."""
    # assert is valid for type narrowing in mypy
    assert isinstance(data, str)
    # mypy knows data is str here, not Union[str, int, None]
    return data.upper()


def guard_clause_narrowing(items: Union[List[str], None]) -> int:
    """Guard clause pattern that looks suspicious but is correct."""
    if items is None:
        return 0
    
    # mypy knows items is List[str] here, not Optional
    return len(items)


def multiple_narrowing_guards(value: Union[int, str, float, None]) -> str:
    """Multiple type guards narrow correctly."""
    if value is None:
        return "none"
    
    if isinstance(value, str):
        # mypy knows Union[int, float, str] here
        return value
    
    if isinstance(value, int):
        # mypy knows Union[float, str] here, but we already handled str
        # so only float remains
        return str(value)
    
    # mypy knows value is float here
    return str(value)


def member_access_after_narrowing(obj: Union[int, str]) -> str:
    """Access methods after correct narrowing."""
    # LLM might flag: this looks wrong
    # But mypy allows it if you check the type first
    if isinstance(obj, str):
        # obj is str, which has these methods
        result = obj.lower()
        return result.replace("a", "b")
    else:
        # obj is int here
        return str(obj)


def union_with_common_methods(val: Union[str, bytes]) -> int:
    """Both str and bytes have len()."""
    # LLM might flag this as uncertain
    # But mypy knows both str and bytes have __len__
    return len(val)


def list_element_type_inference(items: List[Union[int, str]]) -> int:
    """Iterating union elements with proper checks."""
    count = 0
    for item in items:
        if isinstance(item, str):
            # Safe to call str methods
            if item.isdigit():
                count += 1
    return count


def discriminated_union_pattern(data: Union[dict, list]) -> str:
    """Check type once, use throughout."""
    if isinstance(data, dict):
        # mypy narrows to dict for this whole block
        keys = data.keys()
        return str(len(keys))
    else:
        # mypy narrows to list
        return str(len(data))


def chained_isinstance_checks(val: Any) -> str:
    """Chained isinstance for narrowing."""
    if isinstance(val, (int, float)):
        # Can safely use numeric operations
        return str(val + 10)
    elif isinstance(val, str):
        # Can safely use string operations
        return val.upper()
    else:
        return "unknown"


def hasattr_check_is_valid(obj: Any) -> str:
    """LLMs often dismiss hasattr, but it's valid for narrowing in some cases."""
    # While not as reliable as isinstance, hasattr can work
    if hasattr(obj, 'read'):
        # If we're confident about the interface
        return "file-like"
    return "other"


def none_check_with_default(value: Optional[int]) -> int:
    """Correct None handling with truthiness."""
    # This pattern is valid because:
    # - 0 is falsy but still int, so we need "is not None"
    # But here we only care about None, not 0
    if value is not None:
        return value * 2
    return 0


def multiple_checks_combine(val: Union[str, int]) -> str:
    """Multiple conditions that combine safely."""
    # LLM might get confused by the flow
    # But mypy correctly tracks the union through both branches
    if isinstance(val, str):
        return val  # val: str
    else:
        # val: int
        return str(val)


def isinstance_with_inheritance(val: Union[int, str, bool]) -> str:
    """bool is subclass of int, but isinstance still works."""
    # In Python, bool is a subclass of int
    # isinstance checks handle this correctly
    if isinstance(val, bool):
        return "boolean"
    elif isinstance(val, int):
        return "integer"
    else:
        return val  # Must be str


def type_checking_with_try_except(val: Any) -> str:
    """Using exceptions for type narrowing is valid."""
    try:
        # Try to use as string
        return val.upper()
    except AttributeError:
        # Not a string
        try:
            return str(val)
        except:
            return "error"
