"""
Proper Optional handling patterns that LLMs often misunderstand.
These are all valid Python code that mypy accepts.
"""
from typing import Optional, Union, Any, List, Dict, TypeVar, Generic, Callable
import os

T = TypeVar('T')

def get_env_var(name: str) -> Optional[str]:
    """Get environment variable - returns Optional[str]."""
    return os.environ.get(name)

def safe_getenv(name: str) -> str:
    """Safe getenv with default."""
    return get_env_var(name) or "default"

def optional_chaining(user: Optional[Dict[str, Any]]) -> str:
    """Optional chaining with dict access."""
    if user and "name" in user:
        return str(user["name"])
    return "anonymous"

def optional_method_call(obj: Optional[Any]) -> str:
    """Optional method call."""
    if obj and hasattr(obj, 'get_name'):
        return obj.get_name()
    return "unknown"

def optional_attribute_access(obj: Optional[Any]) -> int:
    """Optional attribute access."""
    if obj and hasattr(obj, 'value'):
        return obj.value
    return 0

def optional_indexing(lst: Optional[List[str]]) -> str:
    """Optional list indexing."""
    if lst and len(lst) > 0:
        return lst[0]
    return "empty"

def optional_dict_get(d: Optional[Dict[str, str]], key: str) -> str:
    """Optional dict access."""
    if d:
        return d.get(key, "not found")
    return "no dict"

def union_with_none(value: Union[str, None]) -> str:
    """Union with None is Optional."""
    return value or "none"

def optional_in_conditional(value: Optional[str]) -> bool:
    """Optional in conditional."""
    return value is not None

def optional_length_check(value: Optional[str]) -> int:
    """Optional length check."""
    return len(value) if value else 0

def optional_iteration(items: Optional[List[str]]) -> List[str]:
    """Optional iteration."""
    return items or []

def optional_function_call(func: Optional[Callable[[str], str]], arg: str) -> str:
    """Optional function call."""
    if func:
        return func(arg)
    return arg

def optional_with_default(value: Optional[T], default: T) -> T:
    """Optional with explicit default."""
    return value if value is not None else default

def optional_chained_access(data: Optional[Dict[str, Optional[Dict[str, str]]]]) -> str:
    """Chained optional access."""
    if data:
        user = data.get("user")
        if user and "name" in user:
            return user["name"]
    return "unknown"

def optional_list_comprehension(items: Optional[List[Optional[str]]]) -> List[str]:
    """Optional list comprehension."""
    if items:
        return [item for item in items if item is not None]
    return []

def optional_dict_comprehension(data: Optional[Dict[str, Optional[int]]]) -> Dict[str, int]:
    """Optional dict comprehension."""
    if data:
        return {k: v for k, v in data.items() if v is not None}
    return {}

def optional_set_comprehension(items: Optional[List[Optional[str]]]) -> set:
    """Optional set comprehension."""
    if items:
        return {item for item in items if item is not None}
    return set()

def optional_generator(items: Optional[List[str]]) -> Any:
    """Optional generator."""
    if items:
        for item in items:
            yield item

def optional_with_statement():
    """Optional with statement."""
    path = get_env_var("CONFIG_FILE")
    if path:
        with open(path, 'r') as f:
            return f.read()
    return "no config"

def optional_exception_handling():
    """Optional exception handling."""
    try:
        value = get_env_var("REQUIRED_VAR")
        if value is None:
            raise ValueError("Required var missing")
        return value
    except ValueError:
        return "error"

def optional_type_narrowing(value: Optional[str]) -> str:
    """Optional type narrowing."""
    if value is not None:
        # value is now str
        return value.upper()
    return "none"

def optional_assert(value: Optional[str]) -> str:
    """Optional with assert."""
    assert value is not None, "Value must not be None"
    return value.upper()

def optional_walrus(value: Optional[str]) -> str:
    """Optional with walrus operator."""
    if (result := value) is not None:
        return result.upper()
    return "none"

def optional_in_comprehension(items: Optional[List[Optional[str]]]) -> List[str]:
    """Optional in comprehension."""
    if items:
        return [item.upper() for item in items if item is not None]
    return []

def optional_filter_map(items: Optional[List[Optional[int]]]) -> List[str]:
    """Optional filter and map."""
    if items:
        return [str(x) for x in items if x is not None and x > 0]
    return []

def optional_reduce(items: Optional[List[Optional[int]]]) -> int:
    """Optional reduce."""
    if items:
        valid_items = [x for x in items if x is not None]
        return sum(valid_items) if valid_items else 0
    return 0

def optional_zip(a: Optional[List[str]], b: Optional[List[int]]) -> List[tuple]:
    """Optional zip."""
    if a and b:
        return list(zip(a, b))
    return []

def optional_enumerate(items: Optional[List[str]]) -> List[tuple]:
    """Optional enumerate."""
    if items:
        return list(enumerate(items))
    return []

def optional_reversed(items: Optional[List[str]]) -> List[str]:
    """Optional reversed."""
    if items:
        return list(reversed(items))
    return []

def optional_sorted(items: Optional[List[Optional[int]]]) -> List[int]:
    """Optional sorted."""
    if items:
        valid_items = [x for x in items if x is not None]
        return sorted(valid_items)
    return []

def optional_min_max(items: Optional[List[int]]) -> tuple:
    """Optional min/max."""
    if items and items:
        return min(items), max(items)
    return 0, 0

def optional_any_all(items: Optional[List[bool]]) -> tuple:
    """Optional any/all."""
    if items:
        return any(items), all(items)
    return False, True

def optional_sum(items: Optional[List[Optional[int]]]) -> int:
    """Optional sum."""
    if items:
        return sum(x for x in items if x is not None)
    return 0

def optional_join(items: Optional[List[Optional[str]]]) -> str:
    """Optional join."""
    if items:
        valid_items = [x for x in items if x is not None]
        return ", ".join(valid_items)
    return ""

def optional_format(value: Optional[str]) -> str:
    """Optional format."""
    return f"Value: {value}" if value else "No value"

def optional_json(data: Optional[Any]) -> str:
    """Optional JSON."""
    import json
    if data is not None:
        return json.dumps(data)
    return "{}"

def optional_pickle(data: Optional[Any]) -> bytes:
    """Optional pickle."""
    import pickle
    if data is not None:
        return pickle.dumps(data)
    return b""

def optional_eval(expr: Optional[str]) -> Any:
    """Optional eval."""
    if expr:
        return eval(expr)
    return None

def optional_exec(code: Optional[str]) -> None:
    """Optional exec."""
    if code:
        exec(code)

def optional_import(name: Optional[str]) -> Any:
    """Optional import."""
    if name:
        return __import__(name)
    return None

def optional_getattr(obj: Optional[Any], name: str) -> Any:
    """Optional getattr."""
    if obj is not None:
        return getattr(obj, name, None)
    return None

def optional_setattr(obj: Optional[Any], name: str, value: Any) -> None:
    """Optional setattr."""
    if obj is not None:
        setattr(obj, name, value)

def optional_delattr(obj: Optional[Any], name: str) -> None:
    """Optional delattr."""
    if obj is not None and hasattr(obj, name):
        delattr(obj, name)

def optional_callable(obj: Optional[Any]) -> bool:
    """Optional callable check."""
    return callable(obj) if obj is not None else False

def optional_hash(obj: Optional[Any]) -> int:
    """Optional hash."""
    if obj is not None:
        try:
            return hash(obj)
        except TypeError:
            return 0
    return 0

def optional_dir(obj: Optional[Any]) -> List[str]:
    """Optional dir."""
    if obj is not None:
        return dir(obj)
    return []

def optional_type(obj: Optional[Any]) -> type:
    """Optional type."""
    return type(obj) if obj is not None else type(None)

def optional_id(obj: Optional[Any]) -> int:
    """Optional id."""
    return id(obj) if obj is not None else 0

def optional_repr(obj: Optional[Any]) -> str:
    """Optional repr."""
    return repr(obj) if obj is not None else "None"

def optional_str(obj: Optional[Any]) -> str:
    """Optional str."""
    return str(obj) if obj is not None else ""

def optional_bool(obj: Optional[Any]) -> bool:
    """Optional bool."""
    return bool(obj) if obj is not None else False

def optional_len(obj: Optional[Any]) -> int:
    """Optional len."""
    if obj is not None and hasattr(obj, '__len__'):
        return len(obj)
    return 0

def optional_iter(obj: Optional[Any]) -> Any:
    """Optional iter."""
    if obj is not None:
        try:
            return iter(obj)
        except TypeError:
            return iter([])
    return iter([])

def optional_next(it: Optional[Any]) -> Any:
    """Optional next."""
    if it is not None:
        try:
            return next(it)
        except StopIteration:
            return None
    return None