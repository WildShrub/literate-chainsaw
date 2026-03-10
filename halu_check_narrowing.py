"""
Type narrowing patterns that LLMs often incorrectly flag as errors.
These are all valid Python code that mypy accepts.
"""
from typing import Union, Optional, Any, TypeGuard, cast, TypeVar, Generic
import sys

T = TypeVar('T')

def isinstance_narrowing(value: Union[str, int]) -> str:
    """Valid isinstance narrowing."""
    if isinstance(value, str):
        return value.upper()  # value is narrowed to str
    else:
        return str(value)  # value is narrowed to int

def hasattr_narrowing(obj: Any) -> str:
    """Valid hasattr narrowing."""
    if hasattr(obj, 'upper'):
        return obj.upper()  # obj has upper method
    return str(obj)

def type_guard_example(items: list[Any]) -> list[str]:
    """Valid TypeGuard usage."""
    def is_str_list(lst: list[Any]) -> TypeGuard[list[str]]:
        return all(isinstance(x, str) for x in lst)

    if is_str_list(items):
        return [s.upper() for s in items]  # items is list[str]
    return [str(x) for x in items]

def walrus_narrowing(value: Optional[str]) -> str:
    """Valid walrus operator narrowing."""
    if (result := value) is not None:
        return result.upper()  # result is str
    return "default"

def assert_narrowing(value: Union[str, int]) -> str:
    """Valid assert narrowing."""
    assert isinstance(value, str), "Must be string"
    return value.upper()  # value is narrowed to str

def try_except_narrowing(value: Any) -> str:
    """Valid try/except narrowing."""
    try:
        return value.upper()  # Assume it has upper
    except AttributeError:
        return str(value)

def in_narrowing(container: Union[list[str], dict[str, str]]) -> str:
    """Valid 'in' narrowing."""
    if isinstance(container, dict):
        # container is narrowed to dict[str, str]
        return container.get("key", "default").upper()
    else:
        # container is narrowed to list[str]
        return container[0].upper() if container else "empty"

def callable_check(value: Any) -> str:
    """Valid callable checking."""
    if callable(value):
        return str(type(value))
    return str(value)

def truthiness_narrowing(value: Union[str, list]) -> str:
    """Valid truthiness narrowing."""
    if value:
        if isinstance(value, str):
            return value.upper()
        else:
            return str(len(value))
    return "empty"

def generic_narrowing(container: Any, item: T) -> T:
    """Valid generic narrowing."""
    if isinstance(container, list):
        return item  # T is preserved
    return item

def context_manager_narrowing() -> str:
    """Valid context manager narrowing."""
    with open(__file__, 'r') as f:
        content = f.read()
        if content:
            return content[:10].upper()
    return "empty"

def lambda_narrowing(values: list[Union[str, int]]) -> list[str]:
    """Valid lambda narrowing."""
    strs = [x for x in values if isinstance(x, str)]
    return [s.upper() for s in strs]  # strs is list[str]

def comprehension_narrowing(data: dict[str, Union[str, int]]) -> list[str]:
    """Valid comprehension narrowing."""
    return [v.upper() for v in data.values() if isinstance(v, str)]

def match_statement_narrowing(value: Union[str, int, list]) -> str:
    """Valid match statement narrowing (Python 3.10+)."""
    match value:
        case str():
            return value.upper()  # value is str
        case int():
            return str(value)
        case list():
            return str(len(value))
        case _:
            return "unknown"

def cast_usage(value: Any) -> str:
    """Valid cast usage."""
    result = cast(str, value)
    return result.upper()  # result is treated as str

def overload_narrowing(value: Union[str, int]) -> str:
    """Valid overload narrowing."""
    from typing import overload

    @overload
    def process(x: str) -> str: ...
    @overload
    def process(x: int) -> int: ...

    def process(x):
        return x

    result = process(value)
    if isinstance(result, str):
        return result.upper()
    return str(result)

def any_usage(value: Any) -> Any:
    """Valid Any usage for flexibility."""
    # Any allows any operations
    result = value.upper() if hasattr(value, 'upper') else str(value)
    return result

def union_iteration(items: list[Union[str, int]]) -> list[str]:
    """Valid union iteration with narrowing."""
    results = []
    for item in items:
        if isinstance(item, str):
            results.append(item.upper())
        else:
            results.append(str(item))
    return results

def optional_chaining(value: Optional[dict]) -> str:
    """Valid optional chaining."""
    if value and "key" in value:
        return str(value["key"])
    return "none"

def typevar_narrowing(value: T) -> T:
    """Valid TypeVar narrowing."""
    if isinstance(value, str):
        return value.upper()  # type: ignore  # This is actually valid
    return value