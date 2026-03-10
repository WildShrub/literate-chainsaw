"""
Function overloads and literal types that LLMs often misinterpret.
These patterns look incorrect but are actually valid.
"""
from typing import overload, Literal, Union, Any

@overload
def process_value(value: int) -> str: ...

@overload
def process_value(value: str) -> int: ...

@overload
def process_value(value: float) -> float: ...

def process_value(value):
    """
    LLM might flag: "Overload implementation doesn't match"
    But this is the correct pattern.
    """
    if isinstance(value, int):
        return str(value)
    elif isinstance(value, str):
        return len(value)
    else:
        return value


def test_overloads() -> None:
    """
    LLM might flag: "Wrong return types"
    But overloads narrow correctly.
    """
    # mypy knows these return types
    s: str = process_value(42)
    i: int = process_value("hello")
    f: float = process_value(3.14)
    
    assert s == "42"
    assert i == 5
    assert f == 3.14


@overload
def get_config(key: Literal["debug"]) -> bool: ...

@overload
def get_config(key: Literal["timeout"]) -> int: ...

@overload
def get_config(key: Literal["name"]) -> str: ...

def get_config(key: str) -> Union[bool, int, str]:
    """
    LLM might flag: "Literal types are too restrictive"
    But this is valid for discriminated unions.
    """
    configs = {"debug": True, "timeout": 30, "name": "app"}
    return configs[key]


def use_literal_config() -> None:
    """
    LLM might flag: "get_config returns Union"
    But literals narrow the return type.
    """
    debug: bool = get_config("debug")
    timeout: int = get_config("timeout")
    name: str = get_config("name")
    
    assert debug is True
    assert timeout == 30
    assert name == "app"


@overload
def combine(a: int, b: int) -> int: ...

@overload
def combine(a: str, b: str) -> str: ...

def combine(a, b):
    """
    LLM might flag: "Overload for different types"
    But this is valid.
    """
    return a + b


def test_combine() -> None:
    """Test overloaded combine."""
    num: int = combine(1, 2)
    text: str = combine("a", "b")
    
    assert num == 3
    assert text == "ab"


class Calculator:
    """Calculator with overloaded methods."""
    
    @overload
    def calculate(self, a: int, b: int) -> int: ...
    
    @overload
    def calculate(self, a: str, b: str) -> str: ...
    
    def calculate(self, a, b):
        """Overloaded method."""
        return a + b


def use_calculator() -> None:
    """
    LLM might flag: "Method overloads"
    But this is valid.
    """
    calc = Calculator()
    result1: int = calc.calculate(1, 2)
    result2: str = calc.calculate("a", "b")
    
    assert result1 == 3
    assert result2 == "ab"


def literal_union_function(mode: Literal["add", "multiply"]) -> Callable[[int, int], int]:
    """
    LLM might flag: "Literal in function signature"
    But this is valid for factory functions.
    """
    if mode == "add":
        return lambda x, y: x + y
    else:
        return lambda x, y: x * y


def use_literal_factory() -> None:
    """Use literal-based factory."""
    add_func = literal_union_function("add")
    mul_func = literal_union_function("multiply")
    
    assert add_func(2, 3) == 5
    assert mul_func(2, 3) == 6


@overload
def parse_data(data: str) -> dict: ...

@overload
def parse_data(data: bytes) -> list: ...

def parse_data(data):
    """
    LLM might flag: "Different return types"
    But overloads allow this.
    """
    if isinstance(data, str):
        return {"parsed": data}
    else:
        return [b for b in data]


def test_parse() -> None:
    """Test parse overloads."""
    dict_result: dict = parse_data("hello")
    list_result: list = parse_data(b"hello")
    
    assert dict_result == {"parsed": "hello"}
    assert list_result == [104, 101, 108, 108, 111]


def literal_based_dispatch(action: Literal["start", "stop", "pause"]) -> str:
    """
    LLM might flag: "Literal dispatch"
    But this is a common pattern.
    """
    actions = {
        "start": "Starting...",
        "stop": "Stopping...",
        "pause": "Pausing..."
    }
    return actions[action]


def use_dispatch() -> None:
    """Use literal dispatch."""
    result = literal_based_dispatch("start")
    assert result == "Starting..."


@overload
def filter_items(items: list[int], predicate: Callable[[int], bool]) -> list[int]: ...

@overload
def filter_items(items: list[str], predicate: Callable[[str], bool]) -> list[str]: ...

def filter_items(items, predicate):
    """
    LLM might flag: "Generic overloads"
    But this is valid.
    """
    return [item for item in items if predicate(item)]


def test_filter() -> None:
    """Test filter overloads."""
    numbers: list[int] = filter_items([1, 2, 3, 4], lambda x: x > 2)
    strings: list[str] = filter_items(["a", "bb", "c"], lambda s: len(s) > 1)
    
    assert numbers == [3, 4]
    assert strings == ["bb"]


def literal_with_union(value: Union[Literal["a"], Literal["b"], str]) -> str:
    """
    LLM might flag: "Union with literals"
    But this is valid.
    """
    if value in ("a", "b"):
        return f"special: {value}"
    else:
        return f"other: {value}"


def test_literal_union() -> None:
    """Test literal union."""
    result1 = literal_with_union("a")
    result2 = literal_with_union("other")
    
    assert result1 == "special: a"
    assert result2 == "other: other"


@overload
def transform(value: None) -> None: ...

@overload
def transform(value: int) -> str: ...

@overload
def transform(value: str) -> int: ...

def transform(value):
    """
    LLM might flag: "None overload"
    But this is valid.
    """
    if value is None:
        return None
    elif isinstance(value, int):
        return str(value)
    else:
        return len(value)


def test_transform() -> None:
    """Test transform overloads."""
    none_result: None = transform(None)
    str_result: str = transform(42)
    int_result: int = transform("hello")
    
    assert none_result is None
    assert str_result == "42"
    assert int_result == 5
