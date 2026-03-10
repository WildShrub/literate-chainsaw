"""
Complex type narrowing with multiple conditions that LLMs often misinterpret.
These patterns look error-prone but are actually correct.
"""
from typing import Union, Optional, List

def complex_narrowing(value: Union[int, str, float, None]) -> str:
    """
    LLM might flag: "value could still be None or wrong type"
    But this correctly narrows through multiple checks.
    """
    if value is None:
        return "none"
    if isinstance(value, str):
        return value.upper()
    if isinstance(value, int):
        return str(value)
    # At this point, value must be float
    return f"float: {value}"


def chained_optional_checks(data: Optional[dict[str, Optional[int]]]) -> int:
    """
    LLM might flag: "nested Optional access is unsafe"
    But this is correct with proper checks.
    """
    if data is None:
        return 0
    count = data.get("count")
    if count is None:
        return 0
    return count


def union_with_method_calls(items: Union[List[str], dict[str, str]]) -> int:
    """
    LLM might flag: "can't call len on Union"
    But isinstance narrows correctly.
    """
    if isinstance(items, list):
        return len(items)
    else:
        return len(items)


def assert_based_narrowing(val: Union[str, int]) -> str:
    """
    LLM might flag: "assert doesn't guarantee type"
    But mypy uses assert for narrowing.
    """
    assert isinstance(val, str), "Must be string"
    return val.upper()


def truthiness_narrowing(value: Union[str, int, None]) -> str:
    """
    LLM might flag: "truthiness doesn't narrow Union"
    But for str|int|None, it does narrow to str|int.
    """
    if value:
        # value is not None and not falsy (so not empty str or 0)
        if isinstance(value, str):
            return value
        else:
            return str(value)
    return "empty"


def multiple_isinstance_guards(val: Union[int, str, float]) -> str:
    """
    LLM might flag: "overlapping checks"
    But this correctly handles all cases.
    """
    if isinstance(val, (int, float)):
        return f"number: {val}"
    elif isinstance(val, str):
        return f"text: {val}"
    else:
        return "unknown"


def optional_with_or_operator(value: Optional[str]) -> str:
    """
    LLM might flag: "or operator with None"
    But this is the correct pattern.
    """
    result = value or "default"
    return result.upper()


def dict_access_with_checks(data: dict[str, Union[int, str]]) -> str:
    """
    LLM might flag: "dict access could fail"
    But we check membership first.
    """
    if "key" in data:
        value = data["key"]
        if isinstance(value, str):
            return value
        else:
            return str(value)
    return "missing"


def list_comprehension_with_types(items: List[Union[int, str]]) -> List[str]:
    """
    LLM might flag: "can't convert Union in comprehension"
    But isinstance filters correctly.
    """
    return [str(item) for item in items if isinstance(item, (int, str))]


def function_return_narrowing(func: callable) -> str:
    """
    LLM might flag: "can't call func"
    But we check if it's callable.
    """
    if callable(func):
        result = func()
        return str(result)
    return "not callable"


def attribute_access_with_hasattr(obj: object, attr: str) -> str:
    """
    LLM might flag: "hasattr doesn't guarantee type"
    But this is a valid pattern for dynamic access.
    """
    if hasattr(obj, attr):
        value = getattr(obj, attr)
        return str(value)
    return "no attribute"


def try_except_type_handling(value: Union[int, str]) -> str:
    """
    LLM might flag: "try-except for type checking"
    But this can work for some cases.
    """
    try:
        return value.upper()  # Works if str
    except AttributeError:
        return str(value)  # Fallback for int


def walrus_operator_narrowing(data: Optional[dict]) -> str:
    """
    LLM might flag: "walrus with Optional"
    But this is correct usage.
    """
    if (config := data) is not None and "name" in config:
        return str(config["name"])
    return "unknown"


def conditional_expression_narrowing(val: Union[str, int]) -> str:
    """
    LLM might flag: "conditional doesn't narrow"
    But isinstance in condition does.
    """
    return val.upper() if isinstance(val, str) else str(val)


def loop_with_type_checks(items: List[Union[int, str]]) -> List[str]:
    """
    LLM might flag: "can't iterate Union"
    But List[Union] is fine, and we check inside.
    """
    result = []
    for item in items:
        if isinstance(item, str):
            result.append(item.upper())
        else:
            result.append(str(item))
    return result
