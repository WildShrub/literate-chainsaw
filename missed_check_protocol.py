"""
Protocol implementation errors that LLMs often miss.
These look like they implement protocols but mypy catches violations.
"""
from typing import Protocol, Any, Iterator, Generic, TypeVar

class Writable(Protocol):
    """Protocol for writable objects."""
    
    def write(self, data: str) -> None: ...


class BadWriter:
    """
    LLM might think: "This implements Writable"
    But mypy catches: Missing write method
    """
    def other_method(self) -> None:
        pass


def use_writer(writer: Writable) -> None:
    """Use a writer."""
    writer.write("hello")


def test_bad_writer() -> None:
    """
    LLM might think: "BadWriter has write"
    But mypy catches: Protocol not implemented
    """
    # ERROR: BadWriter doesn't implement Writable
    writer: Writable = BadWriter()  # Type error
    use_writer(writer)


class IterableProtocol(Protocol):
    """Protocol for iterables."""
    
    def __iter__(self) -> Iterator[int]: ...


class BadIterable:
    """
    LLM might think: "This is iterable"
    But mypy catches: Wrong __iter__ return type
    """
    def __iter__(self) -> Iterator[str]:  # ERROR: Should return Iterator[int]
        return iter(["a", "b"])


def use_iterable(items: IterableProtocol) -> int:
    """Sum iterable."""
    return sum(items)


def test_bad_iterable() -> None:
    """
    LLM might think: "BadIterable works"
    But mypy catches: Protocol mismatch
    """
    # ERROR: BadIterable.__iter__ returns Iterator[str], not Iterator[int]
    iterable: IterableProtocol = BadIterable()
    use_iterable(iterable)


class Comparable(Protocol):
    """Protocol for comparable objects."""
    
    def __lt__(self, other: Any) -> bool: ...


class BadComparable:
    """
    LLM might think: "This implements comparison"
    But mypy catches: Missing __lt__ method
    """
    def __eq__(self, other: Any) -> bool:
        return True


def find_min(items: list[Comparable]) -> Comparable:
    """Find minimum."""
    return min(items)


def test_bad_comparable() -> None:
    """
    LLM might think: "BadComparable is comparable"
    But mypy catches: Protocol violation
    """
    # ERROR: BadComparable doesn't implement __lt__
    items: list[Comparable] = [BadComparable()]
    find_min(items)


T = TypeVar('T')

class ContainerProtocol(Protocol[T]):
    """Generic protocol for containers."""
    
    def __getitem__(self, index: int) -> T: ...
    def __len__(self) -> int: ...


class BadContainer(Generic[T]):
    """
    LLM might think: "This implements ContainerProtocol"
    But mypy catches: Missing __len__ method
    """
    def __getitem__(self, index: int) -> T:
        raise IndexError()


def get_first(container: ContainerProtocol[T]) -> T:
    """Get first item."""
    return container[0]


def test_bad_container() -> None:
    """
    LLM might think: "BadContainer works"
    But mypy catches: Missing __len__
    """
    # ERROR: BadContainer doesn't implement __len__
    container: ContainerProtocol[int] = BadContainer[int]()
    get_first(container)


class CallableProtocol(Protocol):
    """Protocol for callables."""
    
    def __call__(self, x: int) -> str: ...


class BadCallable:
    """
    LLM might think: "This is callable"
    But mypy catches: Wrong signature
    """
    def __call__(self, x: str) -> int:  # ERROR: Wrong parameter type
        return len(x)


def apply_callable(func: CallableProtocol, value: int) -> str:
    """Apply callable."""
    return func(value)


def test_bad_callable() -> None:
    """
    LLM might think: "BadCallable matches"
    But mypy catches: Signature mismatch
    """
    # ERROR: BadCallable.__call__ has wrong signature
    func: CallableProtocol = BadCallable()
    apply_callable(func, 42)


class SizedProtocol(Protocol):
    """Protocol for sized objects."""
    
    def __len__(self) -> int: ...


class BadSized:
    """
    LLM might think: "This has __len__"
    But mypy catches: Wrong return type
    """
    def __len__(self) -> str:  # ERROR: Should return int
        return "not int"


def get_size(obj: SizedProtocol) -> int:
    """Get size."""
    return len(obj)


def test_bad_sized() -> None:
    """
    LLM might think: "BadSized works"
    But mypy catches: Wrong return type
    """
    # ERROR: BadSized.__len__ returns str, not int
    obj: SizedProtocol = BadSized()
    get_size(obj)


class HashableProtocol(Protocol):
    """Protocol for hashable objects."""
    
    def __hash__(self) -> int: ...


class BadHashable:
    """
    LLM might think: "This is hashable"
    But mypy catches: Missing __hash__
    """
    def __eq__(self, other: Any) -> bool:
        return True


def use_as_key(obj: HashableProtocol) -> str:
    """Use as dict key."""
    mapping = {obj: "value"}
    return mapping[obj]


def test_bad_hashable() -> None:
    """
    LLM might think: "BadHashable works"
    But mypy catches: Missing __hash__
    """
    # ERROR: BadHashable doesn't implement __hash__
    obj: HashableProtocol = BadHashable()
    use_as_key(obj)


class ContextProtocol(Protocol):
    """Protocol for context managers."""
    
    def __enter__(self) -> Any: ...
    def __exit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> None: ...


class BadContext:
    """
    LLM might think: "This is a context manager"
    But mypy catches: Missing __exit__
    """
    def __enter__(self) -> str:
        return "entered"


def use_context(ctx: ContextProtocol) -> str:
    """Use context manager."""
    with ctx as value:
        return value


def test_bad_context() -> None:
    """
    LLM might think: "BadContext works"
    But mypy catches: Missing __exit__
    """
    # ERROR: BadContext doesn't implement __exit__
    ctx: ContextProtocol = BadContext()
    use_context(ctx)


class SupportsIntProtocol(Protocol):
    """Protocol for int-convertible objects."""
    
    def __int__(self) -> int: ...


class BadSupportsInt:
    """
    LLM might think: "This supports int conversion"
    But mypy catches: Wrong return type
    """
    def __int__(self) -> str:  # ERROR: Should return int
        return "42"


def convert_to_int(obj: SupportsIntProtocol) -> int:
    """Convert to int."""
    return int(obj)


def test_bad_supports_int() -> None:
    """
    LLM might think: "BadSupportsInt works"
    But mypy catches: Wrong return type
    """
    # ERROR: BadSupportsInt.__int__ returns str
    obj: SupportsIntProtocol = BadSupportsInt()
    convert_to_int(obj)


class MapperProtocol(Protocol[T]):
    """Protocol for mappers."""
    
    def map(self, item: T) -> str: ...


class BadMapper:
    """
    LLM might think: "This implements MapperProtocol"
    But mypy catches: Wrong signature
    """
    def map(self, item: int) -> int:  # ERROR: Should return str
        return item * 2


def use_mapper(mapper: MapperProtocol[int], value: int) -> str:
    """Use mapper."""
    return mapper.map(value)


def test_bad_mapper() -> None:
    """
    LLM might think: "BadMapper works"
    But mypy catches: Wrong return type
    """
    # ERROR: BadMapper.map returns int, not str
    mapper: MapperProtocol[int] = BadMapper()
    use_mapper(mapper, 42)
