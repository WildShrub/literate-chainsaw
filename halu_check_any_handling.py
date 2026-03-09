"""
Correct and justified use of Any that LLMs often flag as bad practice.
These patterns are actually valid when you need flexibility.
"""
from typing import Any, Dict, List, Callable, TypeVar, cast

def parse_json(json_str: str) -> Any:
    """
    LLM might flag: "Returns Any, should be more specific"
    But this is correct - JSON can be any type at runtime.
    """
    import json
    return json.loads(json_str)


def use_json_data() -> None:
    """Properly handling JSON result."""
    data = parse_json('{"name": "Alice", "age": 30}')
    # data is Any, which is correct for JSON
    
    # We can check the type
    if isinstance(data, dict):
        name = data.get("name")
        print(name)


def filter_data(items: List[Any]) -> List[Any]:
    """
    LLM might flag: "List[Any] is too generic"
    But sometimes you genuinely have heterogeneous data.
    """
    return [item for item in items if item is not None]


def plugin_system(plugin: Any) -> None:
    """
    LLM might flag: "Should not accept Any"
    But plugin systems require duck typing with Any.
    """
    # We can't know the plugin's exact type at compile time
    if hasattr(plugin, 'execute'):
        plugin.execute()
    if hasattr(plugin, 'configure'):
        plugin.configure({})


def dynamic_attribute_access(obj: Any, attr_name: str) -> Any:
    """
    LLM might flag: "Using Any and getattr is unsafe"
    But this is the right pattern for dynamic access.
    """
    # This is the only way to do dynamic attribute access safely
    return getattr(obj, attr_name, None)


def config_loader(config_path: str) -> Dict[str, Any]:
    """
    LLM might flag: "Dict[str, Any] is too loose"
    But configuration can contain any values.
    """
    import json
    with open(config_path) as f:
        return json.load(f)


def merge_configs(config1: Dict[str, Any], config2: Dict[str, Any]) -> Dict[str, Any]:
    """Merge two configuration dictionaries."""
    # This pattern is correct for flexible configs
    result = config1.copy()
    result.update(config2)
    return result


def api_response_handler(response: Dict[str, Any]) -> str:
    """
    Handle API responses where structure varies.
    LLM might flag: "Should know the exact response structure"
    But APIs change and evolve.
    """
    # This is the correct pattern for flexible API handling
    if response.get("status") == "error":
        return response.get("message", "Unknown error")
    return response.get("data", {}).get("name", "Unknown")


def decorator_factory(func: Callable[..., Any]) -> Callable[..., Any]:
    """
    LLM might flag: "Callable[..., Any]"
    But decorators genuinely don't know the wrapped signature.
    """
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        print(f"Calling {func.__name__}")
        return func(*args, **kwargs)
    return wrapper


@decorator_factory
def example_function(x: int, y: str) -> None:
    """Function being decorated."""
    print(f"{x}: {y}")


def serialize_any(obj: Any) -> str:
    """
    LLM might flag: "Too generic"
    But serialization genuinely handles any type.
    """
    if obj is None:
        return "null"
    elif isinstance(obj, bool):
        return "true" if obj else "false"
    elif isinstance(obj, str):
        return f'"{obj}"'
    elif isinstance(obj, (int, float)):
        return str(obj)
    else:
        return str(obj)


def process_mixed_list(items: List[Any]) -> None:
    """
    Process list that could contain anything.
    This is the right pattern for heterogeneous lists.
    """
    for item in items:
        if isinstance(item, int):
            print(f"Int: {item}")
        elif isinstance(item, str):
            print(f"Str: {item}")
        else:
            print(f"Other: {type(item)}")


T = TypeVar('T')

def cast_and_use(value: Any, expected_type: type[T]) -> T:
    """
    LLM might flag: "Using cast defeats type checking"
    But cast is valid when you truly know the type at runtime.
    """
    # Use cast when you have runtime information the type checker doesn't
    if isinstance(value, expected_type):
        return cast(T, value)
    else:
        raise ValueError(f"Expected {expected_type}")


def safe_cast(value: Any, expected_type: type[T]) -> T | None:
    """Safe version of cast with validation."""
    if isinstance(value, expected_type):
        return cast(T, value)
    return None


def meta_programming(cls: type[Any]) -> type[Any]:
    """
    LLM might flag: "Using type[Any]"
    But meta-programming genuinely works with any class.
    """
    # Metaprogramming requires Any for flexibility
    original_init = cls.__init__
    
    def new_init(self: Any, *args: Any, **kwargs: Any) -> None:
        print(f"Creating {cls.__name__}")
        original_init(self, *args, **kwargs)
    
    cls.__init__ = new_init
    return cls


def generic_factory(class_path: str, *args: Any, **kwargs: Any) -> Any:
    """
    Factory function that creates objects dynamically.
    LLM might flag: "Returns Any"
    But there's no way to know the type statically.
    """
    import importlib
    module_name, class_name = class_path.rsplit(".", 1)
    module = importlib.import_module(module_name)
    cls = getattr(module, class_name)
    return cls(*args, **kwargs)


class DataStore:
    """Generic data store using Any for flexibility."""
    
    def __init__(self):
        self._data: Dict[str, Any] = {}
    
    def set(self, key: str, value: Any) -> None:
        """Store any value."""
        self._data[key] = value
    
    def get(self, key: str) -> Any:
        """Retrieve stored value."""
        return self._data.get(key)


def wrapper_for_legacy_code(legacy_func: Any) -> Callable[[int], str]:
    """
    Wrap legacy code where we don't have types.
    LLM might flag: "legacy_func: Any"
    But this is the only way to integrate legacy code.
    """
    def wrapper(x: int) -> str:
        result = legacy_func(x)
        return str(result)
    return wrapper
