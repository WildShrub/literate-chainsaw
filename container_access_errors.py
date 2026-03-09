"""
Index, slice, and container access errors - mypy catches what runtime inspection often misses.
"""
from typing import Dict, List, Optional, Tuple, TypedDict

def index_errors(items: List[int]) -> None:
    """Accessing list indices incorrectly."""
    # These would all fail at runtime or with mypy
    
    # OK: valid index
    first = items[0]
    
    # No static error, but will be IndexError at runtime
    # mypy doesn't catch this though
    empty_list: List[int] = []
    x = empty_list[0]  # Runtime error, but mypy allows it
    
    # ERROR: slice returns List[int], not int
    sublist: int = items[0:2]


def string_index_errors(text: str) -> None:
    """String indexing."""
    # OK: single char
    char = text[0]
    
    # ERROR: slice returns str, not single char
    first_char: str = text[0:1]  
    two_chars: str = text[0:2]


def negative_index_access(items: List[str]) -> None:
    """Negative indexing."""
    # OK in Python, but mypy checks it
    last = items[-1]
    
    # ERROR: Out of bounds negative index
    # (mypy doesn't always catch, but it's risky)
    very_last = items[-999]


def tuple_unpacking(data: Tuple[int, str, bool]) -> None:
    """Unpacking tuple with wrong sizes."""
    # OK: correct size
    a, b, c = data
    
    # ERROR: unpacking wrong number of values
    x, y = data  # Tuple has 3 elements
    
    # ERROR: unpacking with type mismatch
    x: str
    y: str
    z: str
    x, y, z = data  # z is bool, not str


def dict_access_errors(mapping: Dict[str, int]) -> None:
    """Access dictionary values."""
    # OK: key exists (or we can check)
    if "count" in mapping:
        value = mapping["count"]
    
    # ERROR: Key may not exist, but we access anyway
    missing = mapping["not_there"]  # Could be KeyError
    
    # ERROR: get() returns Optional[int], not int
    value_or_none = mapping.get("key")
    result: int = value_or_none  # None is not int


def dict_type_errors(data: Dict[str, int]) -> None:
    """Manipulate dict with wrong types."""
    # OK: string key, int value
    data["count"] = 42
    
    # ERROR: key should be str, not int
    data[42] = 100
    
    # ERROR: value should be int, not str
    data["name"] = "Alice"


def nested_access_errors() -> None:
    """Access nested structures."""
    # Dict of dicts
    nested: Dict[str, Dict[str, int]] = {
        "user": {"age": 30, "count": 5}
    }
    
    # OK: proper access
    age = nested["user"]["age"]
    
    # ERROR: First dict has str->Dict[str, int], so nested["age"] doesn't exist
    bad = nested["age"]
    
    # ERROR: Second dict has int values, not dicts
    bad2 = nested["user"]["age"]["depth"]


def list_of_dicts_errors() -> None:
    """Work with list of dictionaries."""
    users: List[Dict[str, str]] = [
        {"name": "Alice", "email": "alice@example.com"}
    ]
    
    # OK: access syntax
    first_user = users[0]
    name = first_user["name"]
    
    # ERROR: trying to access list element as if it's dict
    direct = users["name"]
    
    # ERROR: dict value is str, not int
    user_id: int = first_user["email"]


class DataRecord(TypedDict):
    """Typed dict record."""
    id: int
    name: str
    items: List[str]


def typed_dict_access_errors(record: DataRecord) -> None:
    """Access TypedDict with errors."""
    # OK: correct field and type
    item_count = len(record["items"])
    
    # ERROR: 'items' is List[str], trying to access int index
    first_item: int = record["items"][0]
    
    # ERROR: field doesn't exist in TypedDict
    extra = record["extra_field"]
    
    # ERROR: field exists but wrong type access
    bad = record["id"]["value"]  # id is int, not dict


def optional_handling_errors() -> None:
    """Handling Optional types from dict."""
    data: Dict[str, Optional[int]] = {
        "count": 42,
        "missing": None
    }
    
    # ERROR: values are Optional[int], need to handle None
    value = data["count"]
    result: int = value  # Could be None!
    
    # OK: explicit None check  
    if value is not None:
        result = value


def list_comprehension_type_errors() -> None:
    """Type errors in list comprehensions."""
    numbers = [1, 2, 3, 4, 5]
    
    # OK: returns List[int]
    doubled = [n * 2 for n in numbers]
    
    # ERROR: returns List[str], not List[int]
    doubled_wrong: List[int] = [str(n * 2) for n in numbers]
    
    # ERROR: Comprehension with potentially None values
    mixed: List[Optional[int]] = [1, None, 3]
    result: List[int] = [n * 2 for n in mixed]  # Could contain None


def enumerate_errors(items: List[str]) -> None:
    """Enumerate with type errors."""
    # enumerate returns Tuple[int, str]
    for index, item in enumerate(items):
        # OK
        print(f"{index}: {item}")
    
    # ERROR: unpacking wrong
    for item, index in enumerate(items):  # Gets (int, str) but expecting (str, int)
        num: int = item  # item is int, this is OK
        text: str = index  # index is str, not OK


def zip_errors() -> None:
    """Zip with type errors."""
    names = ["Alice", "Bob"]
    ages = [30, 25]
    
    # OK: returns List[Tuple[str, int]]
    for name, age in zip(names, ages):
        print(f"{name} is {age}")
    
    # ERROR: Different lengths/types
    cities = ["NYC", "LA"]
    for name, age, city in zip(names, ages, cities):
        # This works, but if we add a 4th sequence:
        pass
    
    # ERROR: ages is List[int], not List[str]
    for name, age_str in zip(names, ages):
        x: str = age_str  # age_str is int, not str


def default_dict_errors() -> None:
    """Default dict access patterns."""
    # Using dict.get with default
    mapping = {"a": 1, "b": 2}
    
    # OK: returns Optional[int]
    value_maybe = mapping.get("a")
    
    # OK: provides default, returns int
    value_default: int = mapping.get("a", 0)
    
    # ERROR: default type mismatch - expects default same type as values
    bad_default: int = mapping.get("a", "default")  # str != int default type
    
    # ERROR: get with wrong key type
    wrong_key = mapping.get(123)  # Key should be str
