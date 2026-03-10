"""
Complex generic type patterns that LLMs often misunderstand.
These look like type errors but are actually valid.
"""
from typing import TypeVar, Generic, List, Dict, Callable

T = TypeVar('T')
U = TypeVar('U')
V = TypeVar('V')

class Container(Generic[T]):
    """Generic container."""
    
    def __init__(self, value: T):
        self.value = value
    
    def get(self) -> T:
        return self.value
    
    def map(self, func: Callable[[T], U]) -> "Container[U]":
        """Map to different type."""
        return Container(func(self.value))


def generic_function_usage() -> None:
    """
    LLM might flag: "TypeVar inference issues"
    But mypy correctly infers types.
    """
    container = Container(42)  # T=int
    result = container.map(str)  # U=str
    assert result.get() == "42"


class Pair(Generic[T, U]):
    """Generic pair."""
    
    def __init__(self, first: T, second: U):
        self.first = first
        self.second = second
    
    def swap(self) -> "Pair[U, T]":
        """Swap types."""
        return Pair(self.second, self.first)


def pair_operations() -> None:
    """
    LLM might flag: "Type parameters don't match"
    But swap correctly changes types.
    """
    pair = Pair("hello", 42)  # T=str, U=int
    swapped = pair.swap()  # U=str, T=int
    assert swapped.first == 42
    assert swapped.second == "hello"


def higher_order_generics(func: Callable[[T], U], value: T) -> U:
    """
    LLM might flag: "Generic function parameters"
    But this is valid.
    """
    return func(value)


def use_higher_order() -> None:
    """Use higher-order generic function."""
    result = higher_order_generics(str, 123)  # T=int, U=str
    assert result == "123"


class Transformer(Generic[T, U]):
    """Transformer between types."""
    
    def __init__(self, transform: Callable[[T], U]):
        self.transform = transform
    
    def apply(self, value: T) -> U:
        return self.transform(value)


def chained_transforms() -> None:
    """
    LLM might flag: "Complex generic chaining"
    But mypy handles this correctly.
    """
    to_str = Transformer(int, str)(str)
    to_len = Transformer(str, int)(len)
    
    # Chain them
    result = to_len.apply(to_str.apply(42))
    assert result == 2


def generic_with_constraints() -> None:
    """
    LLM might flag: "TypeVar constraints"
    But this is valid usage.
    """
    from typing import TypeVar
    T_constrained = TypeVar('T_constrained', int, str)
    
    def process_constrained(value: T_constrained) -> T_constrained:
        if isinstance(value, int):
            return value * 2  # type: ignore
        else:
            return value.upper()  # type: ignore
    
    # Valid usage
    assert process_constrained(5) == 10
    assert process_constrained("hi") == "HI"


class NestedGeneric(Generic[T]):
    """Nested generic structure."""
    
    def __init__(self, items: List[T]):
        self.items = items
    
    def transform_all(self, func: Callable[[T], U]) -> List[U]:
        """Transform all items."""
        return [func(item) for item in self.items]


def nested_generic_usage() -> None:
    """
    LLM might flag: "Nested generics are complex"
    But this works correctly.
    """
    container = NestedGeneric([1, 2, 3])  # T=int
    result = container.transform_all(str)  # U=str
    assert result == ["1", "2", "3"]


def generic_method_inheritance() -> None:
    """
    LLM might flag: "Inheritance with generics"
    But this is valid.
    """
    class BaseProcessor(Generic[T]):
        def process(self, item: T) -> T:
            return item
    
    class StringProcessor(BaseProcessor[str]):
        def process(self, item: str) -> str:
            return item.upper()
    
    processor = StringProcessor()
    result = processor.process("hello")
    assert result == "HELLO"


def multiple_type_vars() -> None:
    """
    LLM might flag: "Too many TypeVars"
    But this is valid.
    """
    def combine(a: T, b: U, combiner: Callable[[T, U], V]) -> V:
        return combiner(a, b)
    
    result = combine(1, "test", lambda x, y: f"{x}-{y}")
    assert result == "1-test"


class GenericWithDefaults(Generic[T, U]):
    """Generic with default type."""
    
    def __init__(self, first: T, second: U = None):  # type: ignore
        self.first = first
        self.second = second


def use_defaults() -> None:
    """
    LLM might flag: "Default with TypeVar"
    But this can work in some cases.
    """
    obj = GenericWithDefaults("hello")  # T=str, U=None
    assert obj.first == "hello"


def recursive_generic() -> None:
    """
    LLM might flag: "Recursive generics"
    But this is valid.
    """
    class Tree(Generic[T]):
        def __init__(self, value: T, children: List["Tree[T]"] = None):  # type: ignore
            self.value = value
            self.children = children or []
    
    tree = Tree(1, [Tree(2), Tree(3)])
    assert tree.value == 1
    assert len(tree.children) == 2


def bounded_type_vars() -> None:
    """
    LLM might flag: "Bounded TypeVars"
    But this is valid.
    """
    from typing import TypeVar
    NumberT = TypeVar('NumberT', bound=float)
    
    def add_one(num: NumberT) -> NumberT:
        return num + 1  # type: ignore
    
    result = add_one(3.14)
    assert result == 4.14
