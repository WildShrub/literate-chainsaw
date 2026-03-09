"""
Correct Optional and None handling patterns that LLMs often flag as problematic.
"""
from typing import Optional, Union, TypeGuard, overload, Literal

def or_default_pattern(value: Optional[str]) -> str:
    """
    LLM might flag: "value could be None after or"
    But this pattern is actually correct and idiomatic.
    """
    # The 'or' operator is the correct way to provide a default for Optional
    result = value or "default"
    # mypy knows result is str, not Optional[str]
    return result.upper()


def explicit_none_check(value: Optional[int]) -> int:
    """
    LLM might worry about the flow.
    But this is clear and correct.
    """
    if value is not None:
        # mypy knows value is int here
        return value
    return 0


def none_checking_with_complex_default(data: Optional[dict]) -> int:
    """
    LLM might flag: "Could still be None"
    But the pattern is correct.
    """
    config = data or {}
    # config is guaranteed to be dict here
    return len(config)


def late_binding_optional(value: Optional[str]) -> None:
    """
    LLM might worry when we don't check immediately.
    But delaying the check and using value later is fine if we check first.
    """
    if value is None:
        return
    
    # All code after 'return' knows value is not None
    print(value.upper())
    print(value.split(","))


def guard_at_function_entry(value: Optional[int]) -> str:
    """Guard clause pattern - return early if invalid."""
    if value is None:
        return "no value"
    if value < 0:
        return "negative"
    
    # Now value is guaranteed to be a non-negative int
    return f"positive: {value}"


@overload
def get_value(key: str, default: None) -> Optional[str]: ...

@overload
def get_value(key: str, default: str) -> str: ...

def get_value(key: str, default: Optional[str] = None) -> Optional[str]:
    """
    LLM might flag: "Complex overload"
    But this correctly distinguishes return types.
    """
    values = {"a": "alpha", "b": "beta"}
    return values.get(key, default)


def test_overloaded_optional() -> None:
    """Test the overloaded function."""
    # When default is None, result is Optional[str]
    maybe_value = get_value("missing", None)
    
    # When default is provided, result is str
    value = get_value("missing", "default")
    # mypy knows value is str, not Optional[str]
    print(value.upper())


def mixed_optional_operations(items: Optional[list[str]]) -> int:
    """
    LLM might flag: "items could be None"
    But these patterns are correct.
    """
    # Pattern 1: None-coalescing
    safe_items = items or []
    count1 = len(safe_items)
    
    # Pattern 2: Direct None check
    if items is not None:
        count2 = len(items)
    else:
        count2 = 0
    
    return count1 + count2


def optional_in_comprehension(values: list[Optional[int]]) -> list[int]:
    """
    Filter out None values in comprehension.
    LLM might flag: "Some could be None"
    But the filter removes them correctly.
    """
    # This is a correct pattern for filtering None values
    return [v for v in values if v is not None]


def optional_with_method_chain(obj: Optional[dict]) -> str:
    """
    LLM might flag: "Could be None when calling .get()"
    But this is correct and safe.
    """
    # The 'or' ensures dict exists before .get() call
    safe_dict = obj or {}
    return safe_dict.get("name", "unknown")


class Config:
    """Configuration with optional fields."""
    
    def __init__(self, debug: Optional[bool] = None):
        # Store None explicitly
        self.debug = debug
    
    def is_debug_enabled(self) -> bool:
        """
        LLM might flag: "self.debug is Optional[bool]"
        But this is correct - we handle both cases.
        """
        # 'or False' is idiomatic for optional bool
        return self.debug or False


def optional_list_handling(items: Optional[list[str]]) -> None:
    """
    LLM might flag: "items could be None in loop"
    But this is safe.
    """
    # Correct pattern: Default to empty list
    for item in items or []:
        print(item.upper())


def nested_optional_handling(
    outer: Optional[dict[str, Optional[str]]]
) -> str:
    """
    LLM might flag: "Too many Optionals"
    But this is correct handling of nested optionals.
    """
    # First level None check
    if outer is None:
        return "no outer"
    
    # Get with default
    inner_value = outer.get("key")
    
    # Second level None check
    if inner_value is None:
        return "no inner"
    
    return inner_value.upper()


def optional_type_guard(value: Optional[str]) -> TypeGuard[str]:
    """
    Custom type guard for Optional.
    LLM might flag: "Should return bool"
    But TypeGuard correctly types this pattern.
    """
    return value is not None


def use_optional_type_guard(value: Optional[str]) -> None:
    """
    LLM might flag: "value still Optional after guard"
    But TypeGuard narrows it correctly.
    """
    if optional_type_guard(value):
        # mypy knows value is str here due to TypeGuard
        print(value.upper())


def optional_unpacking(data: Optional[tuple[str, int]]) -> Union[str, int]:
    """
    Unpacking Optional tuple.
    LLM might flag: "Could be None"
    But this is correct.
    """
    if data is None:
        return "none"
    
    # Safely unpack because we checked for None
    name, age = data
    return f"{name}: {age}"


def default_factory_pattern(items: Optional[list[str]]) -> list[str]:
    """
    LLM might flag: "items | [] is wrong"
    But the or operator with list is idiomatic and correct.
    """
    # This is the correct way to provide a default for Optional[list]
    return items or []


def optional_with_getattr(obj: Optional[object], attr: str) -> Optional[str]:
    """
    LLM might flag: "obj could be None in getattr"
    But this is safe and correct.
    """
    if obj is None:
        return None
    
    # Safe to use getattr because obj is not None
    return str(getattr(obj, attr, None))


def chain_optional_lookups(data: Optional[dict]) -> Optional[str]:
    """
    Chain of optional accesses.
    LLM might flag: "Intermediate values could be None"
    But this pattern is correct.
    """
    if data is None:
        return None
    
    value = data.get("level1")
    if value is None:
        return None
    
    if isinstance(value, dict):
        return value.get("level2")
    
    return None


def optional_with_walrus(data: Optional[str]) -> int:
    """
    Using :=  (walrus operator) with Optional.
    LLM might flag: "Complex optional handling"
    But this is correct and modern Python.
    """
    if (upper := data) is not None and (length := len(upper)) > 0:
        return length
    return 0
