"""
Proper Any type usage that LLMs often incorrectly flag as problematic.
These are all valid and justified uses of Any in Python typing.
"""
from typing import Any, Union, Optional, Dict, List, cast, TypeVar
import json
import pickle

T = TypeVar('T')

def json_loads(data: str) -> Any:
    """JSON parsing returns Any - this is correct."""
    return json.loads(data)

def json_dumps(obj: Any) -> str:
    """JSON serialization accepts Any - this is correct."""
    return json.dumps(obj)

def pickle_load(file) -> Any:
    """Pickle loading returns Any - this is correct."""
    return pickle.load(file)

def pickle_dump(obj: Any, file) -> None:
    """Pickle dumping accepts Any - this is correct."""
    pickle.dump(obj, file)

def eval_expression(expr: str) -> Any:
    """eval returns Any - this is correct and necessary."""
    return eval(expr)

def exec_code(code: str) -> None:
    """exec accepts Any code - this is correct."""
    exec(code)

def getattr_dynamic(obj: Any, name: str) -> Any:
    """getattr returns Any - this is correct."""
    return getattr(obj, name)

def setattr_dynamic(obj: Any, name: str, value: Any) -> None:
    """setattr accepts Any value - this is correct."""
    setattr(obj, name, value)

def import_module(name: str) -> Any:
    """Import returns Any module - this is correct."""
    return __import__(name)

def create_object(cls: Any, *args, **kwargs) -> Any:
    """Dynamic instantiation returns Any - this is correct."""
    return cls(*args, **kwargs)

def call_method(obj: Any, method_name: str, *args, **kwargs) -> Any:
    """Dynamic method call returns Any - this is correct."""
    method = getattr(obj, method_name)
    return method(*args, **kwargs)

def dict_access(d: Dict[str, Any], key: str) -> Any:
    """Dict with Any values returns Any - this is correct."""
    return d[key]

def list_access(lst: List[Any], index: int) -> Any:
    """List with Any elements returns Any - this is correct."""
    return lst[index]

def union_with_any(value: Union[str, int, Any]) -> Any:
    """Union including Any results in Any - this is correct."""
    return value

def optional_any(value: Optional[Any]) -> Any:
    """Optional[Any] is just Any - this is correct."""
    return value or "default"

def cast_to_any(value: T) -> Any:
    """Cast to Any is always valid - this is correct."""
    return cast(Any, value)

def any_as_type_var(value: Any) -> Any:
    """Any can be assigned to any TypeVar - this is correct."""
    return value

def any_in_generic(container: List[Any]) -> List[Any]:
    """Generic with Any is valid - this is correct."""
    return container

def any_callback(callback: Any, arg: Any) -> Any:
    """Callback with Any signature is valid - this is correct."""
    if callable(callback):
        return callback(arg)
    return arg

def any_exception_handler():
    """Exception handling with Any is valid."""
    try:
        result = json_loads("invalid json")
        return result
    except Exception as e:  # e is Any - this is correct
        return str(e)

def any_mixed_operations(a: Any, b: Any) -> Any:
    """Operations between Any types are valid."""
    return a + b  # Could be anything

def any_attribute_access(obj: Any) -> Any:
    """Attribute access on Any is valid."""
    return obj.any_attribute

def any_indexing(obj: Any) -> Any:
    """Indexing Any is valid."""
    return obj[0]

def any_iteration(obj: Any) -> list:
    """Iterating over Any is valid."""
    return list(obj)

def any_truthiness(obj: Any) -> bool:
    """Checking truthiness of Any is valid."""
    return bool(obj)

def any_type_check(obj: Any) -> str:
    """Type checking Any is valid."""
    return type(obj).__name__

def any_string_conversion(obj: Any) -> str:
    """String conversion of Any is valid."""
    return str(obj)

def any_repr(obj: Any) -> str:
    """Repr of Any is valid."""
    return repr(obj)

def any_hash(obj: Any) -> int:
    """Hash of Any is valid (may raise TypeError)."""
    try:
        return hash(obj)
    except TypeError:
        return 0

def any_equality(a: Any, b: Any) -> bool:
    """Equality comparison of Any is valid."""
    return a == b

def any_identity(a: Any, b: Any) -> bool:
    """Identity comparison of Any is valid."""
    return a is b

def any_in_operator(obj: Any, container: Any) -> bool:
    """'in' operator with Any is valid."""
    return obj in container

def any_method_calls(obj: Any) -> Any:
    """Method calls on Any are valid."""
    return obj.method_that_may_exist()

def any_unpacking(container: Any) -> tuple:
    """Unpacking Any is valid."""
    a, b = container
    return a, b

def any_slicing(obj: Any) -> Any:
    """Slicing Any is valid."""
    return obj[1:5]

def any_formatting(obj: Any) -> str:
    """String formatting with Any is valid."""
    return f"Value: {obj}"

def any_json_like(obj: Any) -> str:
    """Treating Any as JSON-like is valid."""
    return json.dumps({"data": obj})

def any_function_args(func: Any, *args, **kwargs) -> Any:
    """Calling Any as function with Any args is valid."""
    return func(*args, **kwargs)

def any_context_manager(obj: Any):
    """Using Any as context manager is valid."""
    with obj:
        return "done"

def any_descriptor_access(obj: Any) -> Any:
    """Descriptor access on Any is valid."""
    return obj.__get__(None, None)

def any_metaclass_usage(cls: Any) -> Any:
    """Using Any as metaclass is valid."""
    return cls()

def any_module_access(module: Any) -> Any:
    """Accessing Any as module is valid."""
    return module.some_function

def any_class_instantiation(cls: Any) -> Any:
    """Instantiating Any as class is valid."""
    return cls()