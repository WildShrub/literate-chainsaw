"""
Overload and subtle type contextual errors - easy for mypy, hard for LLMs.
"""
from typing import overload, Literal, Union, TypeVar, List

# Overload errors - multiple function signatures

@overload
def process(value: int) -> str: ...

@overload
def process(value: str) -> int: ...

@overload
def process(value: float) -> float: ...

def process(value):  # ERROR: Missing type annotation on parameter
    """Process different types."""
    if isinstance(value, int):
        return str(value)
    elif isinstance(value, str):
        return len(value)
    else:
        return value


def call_process() -> None:
    """Call process with different types."""
    # OK: should work for all these
    s = process(42)
    i = process("hello")
    f = process(3.14)
    
    # These match the overload signatures
    x: str = process(42)  # OK
    y: int = process("hello")  # OK
    z: float = process(3.14)  # OK
    
    # ERROR: process(42) returns str, not int
    bad: int = process(42)
    
    # ERROR: process("hello") returns int, not str  
    bad2: str = process("hello")


# Literal type errors

@overload
def get_value(key: Literal["name"]) -> str: ...

@overload
def get_value(key: Literal["age"]) -> int: ...

@overload
def get_value(key: Literal["active"]) -> bool: ...

def get_value(key: str) -> Union[str, int, bool]:
    """Get value by key."""
    data = {"name": "Alice", "age": 30, "active": True}
    return data.get(key)


def literal_usage() -> None:
    """Use literal types."""
    # OK: mypy knows name returns str
    name: str = get_value("name")
    
    # OK: mypy knows age returns int
    age: int = get_value("age")
    
    # ERROR: mypy doesn't have a Literal overload for "unknown"
    value: str = get_value("unknown")


def with_variable_key() -> None:
    """Using variable keys loses type info."""
    key: str = "name"
    
    # ERROR: mypy can't narrow to specific overload,
    # so result is Union[str, int, bool], not str
    result: str = get_value(key)


# Variable shadowing errors

def shadowing_example() -> None:
    """Shadow variables with different types."""
    value: int = 42
    print(value)
    
    # Later, we reassign to different type
    value = "hello"  # ERROR: Should be int based on original annotation
    
    # This could cause issues
    result: int = value  # ERROR: value is str, not int


def conditional_shadowing(flag: bool) -> None:
    """Shadow in conditional branches."""
    name: str = "Alice"
    
    if flag:
        # ERROR: Reassigning to int instead of str
        name = 42
    
    # mypy sees name as str | int here, but code expects str
    upper = name.upper()


# Loop variable type changes

def loop_type_issue(items: List[Union[int, str]]) -> None:
    """Loop with union types."""
    for item in items:
        # item is int | str here
        # ERROR: int doesn't have .upper()
        print(item.upper())


# Nested type complexity

def nested_complexity(data: Union[List[int], dict[str, str]]) -> int:
    """Work with complex nested types."""
    if isinstance(data, list):
        # data is List[int]
        return len(data)
    else:
        # data is dict[str, str]
        # ERROR: Can't use .values() and subscript with assumed int return
        key = list(data.values())[0]
        return int(key)


T = TypeVar('T')

def first_element(items: List[T]) -> T:
    """Get first element."""
    # ERROR: No bounds checking, could raise IndexError
    return items[0]


def test_first() -> None:
    """Test first element."""
    # OK: returns int since items is List[int]
    x: int = first_element([1, 2, 3])
    
    # OK: returns str since items is List[str]
    y: str = first_element(["a", "b"])
    
    # ERROR: Empty list! But mypy allows it - returns T which could be anything
    z: int = first_element([])


# Return type variance issues

def get_int_list() -> List[int]:
    """Get list of ints."""
    return [1, 2, 3]


def process_items(items: List[Union[int, str]]) -> None:
    """Process list that could contain ints or strings."""
    for item in items:
        print(item)


def variance_issue() -> None:
    """Demonstrate contravariance issue."""
    ints = get_int_list()
    
    # ERROR: List[int] is not List[int | str]
    # Even though List is covariant, process_items expects that
    # we could add a str to the list
    process_items(ints)


# Unreachable code type errors

def unreachable_type_error(x: int) -> str:
    """Code that is unreachable."""
    if x > 0:
        return "positive"
    elif x < 0:
        return "negative"
    elif x == 0:
        return "zero"
    else:
        # ERROR: this is unreachable (x must be > 0, < 0, or == 0)
        # But if we did reach here, what's the type?
        return x  # returns int, not str


# Infinite types and recursive structures

def recursive_issue(n: int) -> int:
    """Recursive call with type issue."""
    if n <= 0:
        return 0
    else:
        # ERROR: recursive call returns int, but we're dividing by string somewhere
        return recursive_issue(n - 1) / "two"  # Type error
