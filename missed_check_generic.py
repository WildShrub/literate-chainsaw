"""
Generic type parameter errors that LLMs often miss.
These look like valid generic code but mypy catches violations.
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


def wrong_type_var_usage() -> None:
    """
    LLM might think: "Container can hold anything"
    But mypy catches: TypeVar constraints violated
    """
    # ERROR: Container expects T, but we're mixing types
    container: Container[int] = Container("string")  # str not int


class Pair(Generic[T, U]):
    """Generic pair."""
    
    def __init__(self, first: T, second: U):
        self.first = first
        self.second = second


def pair_type_mismatch() -> None:
    """
    LLM might think: "Pair can hold different types"
    But mypy catches: Type parameters don't match usage
    """
    # ERROR: Pair[int, str] but assigning wrong types
    pair: Pair[int, str] = Pair("hello", 42)  # Types swapped


def generic_function_mismatch(func: Callable[[T], U], value: T) -> U:
    """
    LLM might think: "Generic function is flexible"
    But mypy catches: Return type doesn't match U
    """
    # ERROR: func returns U, but we're returning T
    return value  # Should return func(value)


def map_container(container: Container[T], mapper: Callable[[T], U]) -> Container[U]:
    """
    LLM might think: "Map function looks correct"
    But mypy catches: Not calling mapper
    """
    # ERROR: Should return Container(mapper(container.get()))
    return Container(container.get())  # Wrong type


class Processor(Generic[T]):
    """Processor for type T."""
    
    def process(self, item: T) -> T:
        return item


def wrong_inheritance() -> None:
    """
    LLM might think: "Subclass can override"
    But mypy catches: Return type incompatible with base
    """
    class StringProcessor(Processor[str]):
        def process(self, item: str) -> int:  # ERROR: Should return str
            return len(item)
    
    processor = StringProcessor()
    result: str = processor.process("hello")  # Expects str, gets int


def nested_generic_error() -> None:
    """
    LLM might think: "Nested generics work"
    But mypy catches: Type parameter mismatch
    """
    class NestedContainer(Generic[T]):
        def __init__(self, items: List[T]):
            self.items = items
        
        def get_first(self) -> T:
            return self.items[0]
    
    # ERROR: NestedContainer expects List[T], getting List[str]
    container: NestedContainer[int] = NestedContainer(["a", "b"])  # Wrong inner type


def type_var_constraint_violation() -> None:
    """
    LLM might think: "TypeVar without constraints is flexible"
    But mypy catches: Constraint violations
    """
    T_constrained = TypeVar('T_constrained', int, str)
    
    def process_constrained(value: T_constrained) -> T_constrained:
        # ERROR: Can't call .upper() on T_constrained (could be int)
        return value.upper()  # type: ignore
    
    # This would work at runtime but mypy catches it
    result: int = process_constrained(42)  # 42.upper() fails


def generic_method_error() -> None:
    """
    LLM might think: "Method is generic"
    But mypy catches: Type parameter issues
    """
    class Transformer(Generic[T, U]):
        def transform(self, value: T) -> U:
            # ERROR: Can't convert T to U without proper mapping
            return value  # Type mismatch
    
    transformer = Transformer[int, str]()
    result: str = transformer.transform(42)  # Gets int, expects str


def higher_order_generic_error(func: Callable[[T], T], value: T) -> T:
    """
    LLM might think: "Function preserves type"
    But mypy catches: func might not preserve T
    """
    # ERROR: func: Callable[[T], T] but we don't know if it actually returns T
    return func(value)  # This is actually fine, but let's make error


def dict_generic_error(data: Dict[T, U]) -> U:
    """
    LLM might think: "Dict access returns U"
    But mypy knows: Dict access returns U | None, not U
    """
    # ERROR: data[T] returns U, but key might not exist
    return data["missing_key"]  # KeyError possible, type is U but could be missing


def list_generic_error(items: List[T]) -> T:
    """
    LLM might think: "List access is safe"
    But mypy knows: Index could be out of bounds
    """
    # ERROR: items[0] could raise IndexError, but type is T
    return items[0]  # Runtime error if empty


def callable_generic_error(func: Callable[[T], U], arg: T) -> U:
    """
    LLM might think: "Callable returns U"
    But mypy can't verify the actual return type
    """
    # ERROR: func might not actually return U
    return func(arg)


def bounded_type_var_error() -> None:
    """
    LLM might think: "Bounded TypeVar works"
    But mypy catches: Operations not available on bound
    """
    from typing import TypeVar
    NumberT = TypeVar('NumberT', bound=float)
    
    def add_to_number(num: NumberT) -> NumberT:
        # ERROR: Can't assume all bound types support +
        return num + 1  # type: ignore
    
    result = add_to_number(3.14)
    # This works but mypy might flag depending on strictness


def contravariant_error() -> None:
    """
    LLM might think: "Contravariance allows this"
    But mypy catches: Wrong variance direction
    """
    T_contra = TypeVar('T_contra', contravariant=True)
    
    class Consumer(Generic[T_contra]):
        def consume(self, item: T_contra) -> None:
            pass
    
    # ERROR: Variance mismatch
    consumer: Consumer[int] = Consumer()  # Type issues


def recursive_generic_error() -> None:
    """
    LLM might think: "Recursive generic is fine"
    But mypy catches: Type recursion issues
    """
    class Tree(Generic[T]):
        def __init__(self, value: T, children: List["Tree[T]"] = None):
            self.value = value
            self.children = children or []
    
    # ERROR: Type recursion can cause issues
    tree = Tree(1, [Tree("string")])  # Mixed types in recursion


def generic_with_any_error() -> None:
    """
    LLM might think: "Any makes it flexible"
    But mypy catches: Any doesn't solve type issues
    """
    from typing import Any
    
    def process_any(value: Any) -> int:
        # ERROR: Any doesn't guarantee int return
        return value + 1  # value could be str
    
    result = process_any("hello")  # Runtime error
