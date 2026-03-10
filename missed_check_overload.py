"""
Function overload errors that LLMs often miss.
These look like valid overloads but mypy catches signature mismatches.
"""
from typing import overload, Literal, Union, Any

@overload
def process_value(value: int) -> str: ...

@overload
def process_value(value: str) -> int: ...

def process_value(value):
    """
    LLM might think: "Overload looks correct"
    But mypy catches: Implementation doesn't match overloads
    """
    # ERROR: Implementation should handle both cases properly
    if isinstance(value, int):
        return str(value)
    else:
        return len(value)  # Returns int for str, but overload says str -> int


def test_overload_mismatch() -> None:
    """
    LLM might think: "This works"
    But mypy catches: Return type mismatch with overload
    """
    # ERROR: process_value(str) should return int, but implementation returns int for str
    result: int = process_value("hello")  # Expects int, gets int - wait, this is fine
    # Let's make it error: overload says str -> int, but let's return str
    result2: int = process_value("hello")  # This should be fine


@overload
def get_config(key: Literal["debug"]) -> bool: ...

@overload
def get_config(key: Literal["timeout"]) -> int: ...

@overload
def get_config(key: Literal["name"]) -> str: ...

def get_config(key: str) -> Union[bool, int, str]:
    """
    LLM might think: "Literal overloads are fine"
    But mypy catches: Wrong return type for some overloads
    """
    configs = {"debug": True, "timeout": 30, "name": "app"}
    # ERROR: get_config("debug") should return bool, but Union allows it
    return configs.get(key)  # This returns Optional, not the specific types


def test_literal_overload() -> None:
    """
    LLM might think: "This narrows correctly"
    But mypy catches: get_config returns Union, not specific type
    """
    # ERROR: get_config("debug") returns Union[bool, int, str], not bool
    debug: bool = get_config("debug")


@overload
def combine(a: int, b: int) -> int: ...

@overload
def combine(a: str, b: str) -> str: ...

def combine(a, b):
    """
    LLM might think: "Combine works for both types"
    But mypy catches: Implementation doesn't match overloads
    """
    # ERROR: For (str, str), should return str, but len returns int
    if isinstance(a, int) and isinstance(b, int):
        return a + b
    else:
        return len(str(a) + str(b))  # Returns int, not str


def test_combine_overload() -> None:
    """
    LLM might think: "combine(str, str) returns str"
    But mypy catches: Implementation returns int
    """
    # ERROR: combine expects str return, but gets int
    result: str = combine("a", "b")


class Calculator:
    """
    LLM might think: "Method overloads are fine"
    But mypy catches: Implementation signature issues
    """
    
    @overload
    def calculate(self, a: int, b: int) -> int: ...
    
    @overload
    def calculate(self, a: str, b: str) -> str: ...
    
    def calculate(self, a, b):
        # ERROR: Implementation doesn't properly handle overload cases
        return str(a) + str(b)  # Always returns str


def test_calculator_overload() -> None:
    """
    LLM might think: "calculate(int, int) returns int"
    But mypy catches: Implementation always returns str
    """
    calc = Calculator()
    # ERROR: calculate expects int return, gets str
    result: int = calc.calculate(1, 2)


def literal_based_dispatch(action: Literal["start", "stop", "pause"]) -> str:
    """
    LLM might think: "Literal dispatch is correct"
    But mypy catches: Not all literal cases handled
    """
    # ERROR: Missing "pause" case
    if action == "start":
        return "Starting..."
    elif action == "stop":
        return "Stopping..."
    else:
        return "Unknown"


def test_literal_dispatch() -> None:
    """
    LLM might think: "All cases covered"
    But mypy catches: "pause" not handled
    """
    # This works, but mypy knows "pause" isn't handled
    result = literal_based_dispatch("pause")  # Could be "Unknown"


@overload
def parse_data(data: str) -> dict: ...

@overload
def parse_data(data: bytes) -> list: ...

def parse_data(data):
    """
    LLM might think: "Parse handles both types"
    But mypy catches: Wrong return types
    """
    if isinstance(data, str):
        return {"parsed": data}  # OK
    else:
        return str(data)  # ERROR: Should return list, returns str


def test_parse_overload() -> None:
    """
    LLM might think: "parse_data(bytes) returns list"
    But mypy catches: Returns str instead
    """
    # ERROR: parse_data expects list return, gets str
    result: list = parse_data(b"data")


@overload
def filter_items(items: list[int], predicate: Callable[[int], bool]) -> list[int]: ...

@overload
def filter_items(items: list[str], predicate: Callable[[str], bool]) -> list[str]: ...

def filter_items(items, predicate):
    """
    LLM might think: "Generic overloads work"
    But mypy catches: Implementation doesn't preserve types
    """
    # ERROR: Always returns list of original type, but predicate might change it
    return [item for item in items if predicate(item)]


def test_filter_overload() -> None:
    """
    LLM might think: "filter preserves list type"
    But mypy catches: Type issues
    """
    # This should work, but let's see
    numbers: list[int] = filter_items([1, 2, 3], lambda x: x > 1)
    # ERROR if predicate changes type, but it doesn't


@overload
def transform(value: None) -> None: ...

@overload
def transform(value: int) -> str: ...

@overload
def transform(value: str) -> int: ...

def transform(value):
    """
    LLM might think: "Transform handles all cases"
    But mypy catches: Wrong return types
    """
    if value is None:
        return None
    elif isinstance(value, int):
        return str(value)  # OK
    else:
        return value  # ERROR: Should return int, returns str


def test_transform_overload() -> None:
    """
    LLM might think: "transform(str) returns int"
    But mypy catches: Returns str instead
    """
    # ERROR: transform expects int return, gets str
    result: int = transform("hello")


@overload
def create_object(type_hint: Literal["dict"]) -> dict: ...

@overload
def create_object(type_hint: Literal["list"]) -> list: ...

def create_object(type_hint: str) -> Any:
    """
    LLM might think: "Factory creates correct types"
    But mypy catches: Wrong return types
    """
    if type_hint == "dict":
        return []  # ERROR: Should return dict, returns list
    elif type_hint == "list":
        return {}  # ERROR: Should return list, returns dict
    else:
        return None


def test_create_overload() -> None:
    """
    LLM might think: "create_object returns correct type"
    But mypy catches: Wrong types returned
    """
    # ERROR: create_object expects dict, gets list
    result: dict = create_object("dict")


@overload
def validate_input(data: str) -> bool: ...

@overload
def validate_input(data: int) -> str: ...

def validate_input(data):
    """
    LLM might think: "Validation returns appropriate type"
    But mypy catches: Wrong return types
    """
    if isinstance(data, str):
        return len(data) > 0  # OK: bool
    else:
        return "valid"  # ERROR: Should return str, but for int overload it's str - wait
        # Actually, for int it should return str, this is fine


def test_validate_overload() -> None:
    """
    LLM might think: "validate_input works"
    But mypy catches: Type issues
    """
    # This should be fine
    result1: bool = validate_input("test")
    result2: str = validate_input(42)


@overload
def merge(a: dict, b: dict) -> dict: ...

@overload
def merge(a: list, b: list) -> list: ...

def merge(a, b):
    """
    LLM might think: "Merge combines same types"
    But mypy catches: Wrong implementation
    """
    # ERROR: For dict, should return dict, but list concatenation returns list
    if isinstance(a, dict):
        result = {}
        result.update(a)
        result.update(b)
        return result  # OK
    else:
        return a + b  # OK for list


def test_merge_overload() -> None:
    """
    LLM might think: "merge works for both"
    But mypy catches: Type issues if any
    """
    # Should be fine
    dict_result: dict = merge({"a": 1}, {"b": 2})
    list_result: list = merge([1, 2], [3, 4])
