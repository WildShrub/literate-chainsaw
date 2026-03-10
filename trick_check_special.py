"""
Special typing constructs that LLMs often misunderstand.
These look like errors but are actually valid advanced typing.
"""
from typing import TypeGuard, cast, Any, Union, Literal, overload, TypeVar, Generic

def is_string(value: Any) -> TypeGuard[str]:
    """
    LLM might flag: "TypeGuard return type"
    But TypeGuard is valid for narrowing.
    """
    return isinstance(value, str)


def process_value(value: Any) -> str:
    """
    LLM might flag: "value still Any after check"
    But TypeGuard narrows it.
    """
    if is_string(value):
        # mypy knows value is str here
        return value.upper()
    else:
        return str(value)


def test_type_guard() -> None:
    """Test TypeGuard."""
    result1 = process_value("hello")
    result2 = process_value(42)
    
    assert result1 == "HELLO"
    assert result2 == "42"


def safe_cast(value: Any, target_type: type) -> Any:
    """
    LLM might flag: "Using cast is unsafe"
    But cast is valid when you know the type.
    """
    if isinstance(value, target_type):
        return cast(target_type, value)
    raise ValueError(f"Not a {target_type}")


def test_safe_cast() -> None:
    """Test safe cast."""
    result: int = safe_cast("42", int)  # This would fail at runtime
    # But the typing is correct for the pattern


def literal_based_switch(value: Union[Literal["a"], Literal["b"], str]) -> str:
    """
    LLM might flag: "Union with literals is confusing"
    But this is valid discriminated union.
    """
    if value == "a":
        return "option a"
    elif value == "b":
        return "option b"
    else:
        return f"other: {value}"


def test_literal_switch() -> None:
    """Test literal switch."""
    result1 = literal_based_switch("a")
    result2 = literal_based_switch("other")
    
    assert result1 == "option a"
    assert result2 == "other: other"


T = TypeVar('T')

def identity(value: T) -> T:
    """
    LLM might flag: "Simple identity function"
    But TypeVar identity is valid.
    """
    return value


def test_identity() -> None:
    """Test identity function."""
    result: str = identity("hello")
    assert result == "hello"


class TypeVarContainer(Generic[T]):
    """Container with TypeVar."""
    
    def __init__(self, value: T):
        self.value = value
    
    def get(self) -> T:
        return self.value


def use_type_var_container() -> None:
    """
    LLM might flag: "Generic container"
    But this is standard.
    """
    container = TypeVarContainer("test")
    result: str = container.get()
    assert result == "test"


def dynamic_attribute_access(obj: Any, attr: str) -> Any:
    """
    LLM might flag: "getattr is unsafe"
    But this is valid for dynamic access.
    """
    return getattr(obj, attr, None)


def test_dynamic_access() -> None:
    """Test dynamic access."""
    class TestObj:
        def __init__(self):
            self.name = "test"
    
    obj = TestObj()
    result = dynamic_attribute_access(obj, "name")
    assert result == "test"


@overload
def overloaded_factory(mode: Literal["int"]) -> int: ...

@overload
def overloaded_factory(mode: Literal["str"]) -> str: ...

def overloaded_factory(mode: str) -> Any:
    """
    LLM might flag: "Overload with literals"
    But this is valid factory pattern.
    """
    if mode == "int":
        return 42
    elif mode == "str":
        return "hello"
    else:
        return None


def test_overloaded_factory() -> None:
    """Test overloaded factory."""
    int_result: int = overloaded_factory("int")
    str_result: str = overloaded_factory("str")
    
    assert int_result == 42
    assert str_result == "hello"


def walrus_with_type_narrowing(data: Union[dict, None]) -> str:
    """
    LLM might flag: "Walrus operator with Optional"
    But this is valid.
    """
    if (config := data) is not None and "key" in config:
        return str(config["key"])
    return "default"


def test_walrus_narrowing() -> None:
    """Test walrus narrowing."""
    data = {"key": "value"}
    result = walrus_with_type_narrowing(data)
    assert result == "value"


def cast_for_runtime_knowledge(value: Any) -> int:
    """
    LLM might flag: "cast defeats type checking"
    But cast is valid when you have runtime guarantees.
    """
    # Assume we know this is int at runtime
    return cast(int, value)


def test_cast() -> None:
    """Test cast usage."""
    # In real code, you'd have runtime checks
    result = cast_for_runtime_knowledge(42)
    assert result == 42


def union_with_callable(value: Union[Callable[[], str], str]) -> str:
    """
    LLM might flag: "Union with callable"
    But this is valid.
    """
    if callable(value):
        return value()
    else:
        return value


def test_union_callable() -> None:
    """Test union with callable."""
    result1 = union_with_callable(lambda: "called")
    result2 = union_with_callable("string")
    
    assert result1 == "called"
    assert result2 == "string"


def generic_with_new_type() -> None:
    """
    LLM might flag: "Complex generic usage"
    But this is valid.
    """
    from typing import NewType
    
    UserId = NewType('UserId', int)
    
    def get_user(id: UserId) -> str:
        return f"user_{id}"
    
    user_id = UserId(123)
    result = get_user(user_id)
    assert result == "user_123"


def protocol_with_generic() -> None:
    """
    LLM might flag: "Protocol with generic"
    But this is valid.
    """
    from typing import Protocol
    
    class Mapper(Protocol[T]):
        def map(self, item: T) -> str: ...
    
    class StringMapper:
        def map(self, item: str) -> str:
            return item.upper()
    
    def use_mapper(mapper: Mapper[str], value: str) -> str:
        return mapper.map(value)
    
    mapper = StringMapper()
    result = use_mapper(mapper, "hello")
    assert result == "HELLO"


def final_test() -> None:
    """Run all tests."""
    test_type_guard()
    test_safe_cast()
    test_literal_switch()
    test_identity()
    use_type_var_container()
    test_dynamic_access()
    test_overloaded_factory()
    test_walrus_narrowing()
    test_cast()
    test_union_callable()
    generic_with_new_type()
    protocol_with_generic()
    
    print("All tests passed!")


if __name__ == "__main__":
    final_test()
