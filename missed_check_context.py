"""
Context-dependent type errors that LLMs often miss.
These look correct in isolation but mypy catches contextual issues.
"""
from typing import TypeGuard, cast, Any, Union, Literal, overload, TypeVar, Generic

def is_string(value: Any) -> TypeGuard[str]:
    """
    LLM might think: "TypeGuard correctly narrows"
    But mypy catches: TypeGuard not properly used
    """
    return isinstance(value, str)


def wrong_type_guard_usage(value: Any) -> str:
    """
    LLM might think: "is_string narrows value to str"
    But mypy catches: TypeGuard not narrowing properly
    """
    if is_string(value):
        # ERROR: value should be str here, but mypy may not narrow
        return value.upper()
    else:
        # ERROR: value could still be str in some cases
        return str(value)


def test_type_guard() -> None:
    """Test TypeGuard."""
    result = wrong_type_guard_usage("hello")
    # This works, but mypy might not catch issues


def safe_cast(value: Any, target_type: type) -> Any:
    """
    LLM might think: "cast ensures type safety"
    But mypy catches: cast doesn't validate at runtime
    """
    if isinstance(value, target_type):
        return cast(target_type, value)
    raise ValueError(f"Not a {target_type}")


def wrong_cast_usage() -> None:
    """
    LLM might think: "cast makes it safe"
    But mypy catches: cast bypasses type checking
    """
    # ERROR: cast tells mypy it's int, but it's str
    result: int = cast(int, "not a number")
    # Runtime error, but mypy trusts cast


def literal_union(value: Union[Literal["a"], Literal["b"], str]) -> str:
    """
    LLM might think: "Union with literals works"
    But mypy catches: str overlaps with literals
    """
    if value == "a":
        return "option a"
    elif value == "b":
        return "option b"
    else:
        # ERROR: value could be "a" or "b" already handled
        return f"other: {value}"


def test_literal_union() -> None:
    """Test literal union."""
    # mypy may not catch that "a" is already handled
    result = literal_union("a")


T = TypeVar('T')

def identity(value: T) -> T:
    """
    LLM might think: "Identity preserves type"
    But mypy catches: TypeVar inference issues
    """
    return value


def wrong_identity_usage() -> None:
    """
    LLM might think: "identity returns same type"
    But mypy catches: Type inference problems
    """
    # ERROR: identity should preserve type, but mypy might infer wrong
    result: str = identity(42)  # 42 is int, not str


class TypeVarContainer(Generic[T]):
    """Container with TypeVar."""
    
    def __init__(self, value: T):
        self.value = value
    
    def get(self) -> T:
        return self.value


def wrong_type_var_inference() -> None:
    """
    LLM might think: "TypeVar infers correctly"
    But mypy catches: Wrong type inference
    """
    container = TypeVarContainer(42)  # T should be int
    # ERROR: container.get() should return int, not str
    result: str = container.get()


def dynamic_attribute_access(obj: Any, attr: str) -> Any:
    """
    LLM might think: "getattr is dynamic"
    But mypy catches: Any return type issues
    """
    return getattr(obj, attr, None)


def wrong_dynamic_access() -> None:
    """
    LLM might think: "getattr returns correct type"
    But mypy catches: Any doesn't guarantee type
    """
    class TestObj:
        def __init__(self):
            self.value = 42
    
    obj = TestObj()
    # ERROR: getattr returns Any, not int
    result: int = dynamic_attribute_access(obj, "value")


@overload
def overloaded_factory(mode: Literal["int"]) -> int: ...

@overload
def overloaded_factory(mode: Literal["str"]) -> str: ...

def overloaded_factory(mode: str) -> Any:
    """
    LLM might think: "Overloads handle all cases"
    But mypy catches: Implementation return type issues
    """
    if mode == "int":
        return 42
    elif mode == "str":
        return "hello"
    else:
        # ERROR: Returns Any, but overloads don't cover other modes
        return None


def wrong_overloaded_usage() -> None:
    """
    LLM might think: "Factory returns correct type"
    But mypy catches: Wrong type for unhandled modes
    """
    # ERROR: overloaded_factory("other") returns Any, not handled by overloads
    result: int = overloaded_factory("other")


def walrus_with_type(value: Union[str, int]) -> str:
    """
    LLM might think: "walrus assigns and checks"
    But mypy catches: Walrus type narrowing issues
    """
    if (text := value) and isinstance(text, str):
        return text
    else:
        # ERROR: text could be int or falsy str
        return str(text)


def test_walrus() -> None:
    """Test walrus."""
    result = walrus_with_type(42)
    # mypy may not catch that text could be int


def union_with_callable(value: Union[Callable[[], str], str]) -> str:
    """
    LLM might think: "Union handles both cases"
    But mypy catches: Callable not checked properly
    """
    if callable(value):
        return value()
    else:
        # ERROR: value could still be callable in some cases
        return value


def test_union_callable() -> None:
    """Test union callable."""
    # mypy may not catch edge cases
    result = union_with_callable("string")


def generic_with_new_type() -> None:
    """
    LLM might think: "NewType works like alias"
    But mypy catches: NewType is distinct type
    """
    from typing import NewType
    
    UserId = NewType('UserId', int)
    
    def get_user(id: UserId) -> str:
        return f"user_{id}"
    
    # ERROR: int is not UserId, even though NewType is based on int
    user_id = UserId(123)  # OK
    wrong_id: UserId = 456  # ERROR: int is not UserId


def protocol_with_generic() -> None:
    """
    LLM might think: "Protocol matches structurally"
    But mypy catches: Protocol not implemented
    """
    from typing import Protocol
    
    class Mapper(Protocol[T]):
        def map(self, item: T) -> str: ...
    
    class WrongMapper:
        def map(self, item: int) -> int:  # Wrong return type
            return item * 2
    
    def use_mapper(mapper: Mapper[int], value: int) -> str:
        return mapper.map(value)
    
    # ERROR: WrongMapper doesn't implement Mapper[int] correctly
    mapper: Mapper[int] = WrongMapper()
    use_mapper(mapper, 42)


def final_test() -> None:
    """Run all tests."""
    wrong_type_guard_usage("test")
    wrong_cast_usage()
    test_literal_union()
    wrong_identity_usage()
    wrong_type_var_inference()
    wrong_dynamic_access()
    wrong_overloaded_usage()
    test_walrus()
    test_union_callable()
    generic_with_new_type()
    protocol_with_generic()
    
    print("All tests completed (with errors)")


if __name__ == "__main__":
    final_test()
