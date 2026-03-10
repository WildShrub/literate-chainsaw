"""
Protocol and structural typing that LLMs often misunderstand.
These look like inheritance errors but are actually valid.
"""
from typing import Protocol, Any, Iterator, Generic, TypeVar

class Writable(Protocol):
    """Protocol for writable objects."""
    
    def write(self, data: str) -> None: ...


class FileWriter:
    """Implements Writable without inheriting."""
    
    def __init__(self, filename: str):
        self.filename = filename
    
    def write(self, data: str) -> None:
        with open(self.filename, 'a') as f:
            f.write(data)


def use_writer(writer: Writable) -> None:
    """
    LLM might flag: "FileWriter doesn't inherit from Writable"
    But structural typing allows it.
    """
    writer.write("Hello")


def test_protocol() -> None:
    """Test protocol usage."""
    writer = FileWriter("test.txt")
    use_writer(writer)  # Works despite no inheritance


class IterableProtocol(Protocol):
    """Protocol for iterables."""
    
    def __iter__(self) -> Iterator[int]: ...


class CustomRange:
    """Custom range that implements IterableProtocol."""
    
    def __init__(self, start: int, end: int):
        self.start = start
        self.end = end
    
    def __iter__(self) -> Iterator[int]:
        for i in range(self.start, self.end):
            yield i


def sum_iterable(items: IterableProtocol) -> int:
    """
    LLM might flag: "CustomRange not iterable"
    But it implements the protocol.
    """
    return sum(items)


def test_custom_iterable() -> None:
    """Test custom iterable."""
    custom_range = CustomRange(1, 4)
    result = sum_iterable(custom_range)
    assert result == 6


class Comparable(Protocol):
    """Protocol for comparable objects."""
    
    def __lt__(self, other: Any) -> bool: ...


class Version:
    """Version class that implements comparison."""
    
    def __init__(self, major: int, minor: int):
        self.major = major
        self.minor = minor
    
    def __lt__(self, other: "Version") -> bool:
        if self.major != other.major:
            return self.major < other.major
        return self.minor < other.minor


def find_min(items: list[Comparable]) -> Comparable:
    """
    LLM might flag: "Version not Comparable"
    But it implements the protocol.
    """
    return min(items)


def test_comparable() -> None:
    """Test comparable protocol."""
    versions = [Version(1, 2), Version(1, 1), Version(2, 0)]
    min_version = find_min(versions)
    assert min_version.major == 1 and min_version.minor == 1


T = TypeVar('T')

class ContainerProtocol(Protocol[T]):
    """Generic protocol for containers."""
    
    def __getitem__(self, index: int) -> T: ...
    def __len__(self) -> int: ...


class SimpleList(Generic[T]):
    """Simple list implementing ContainerProtocol."""
    
    def __init__(self, items: list[T]):
        self.items = items
    
    def __getitem__(self, index: int) -> T:
        return self.items[index]
    
    def __len__(self) -> int:
        return len(self.items)


def get_first(container: ContainerProtocol[T]) -> T:
    """
    LLM might flag: "SimpleList not ContainerProtocol"
    But it implements the protocol.
    """
    return container[0]


def test_generic_protocol() -> None:
    """Test generic protocol."""
    my_list = SimpleList([1, 2, 3])
    first: int = get_first(my_list)
    assert first == 1


class CallableProtocol(Protocol):
    """Protocol for callables."""
    
    def __call__(self, x: int) -> str: ...


class Multiplier:
    """Multiplier that implements CallableProtocol."""
    
    def __init__(self, factor: int):
        self.factor = factor
    
    def __call__(self, x: int) -> str:
        return str(x * self.factor)


def apply_callable(func: CallableProtocol, value: int) -> str:
    """
    LLM might flag: "Multiplier not callable in type sense"
    But it implements the protocol.
    """
    return func(value)


def test_callable_protocol() -> None:
    """Test callable protocol."""
    multiplier = Multiplier(3)
    result = apply_callable(multiplier, 5)
    assert result == "15"


class SizedProtocol(Protocol):
    """Protocol for sized objects."""
    
    def __len__(self) -> int: ...


class CustomSized:
    """Custom sized object."""
    
    def __init__(self, size: int):
        self.size = size
    
    def __len__(self) -> int:
        return self.size


def get_size(obj: SizedProtocol) -> int:
    """
    LLM might flag: "CustomSized not SizedProtocol"
    But it implements the protocol.
    """
    return len(obj)


def test_sized_protocol() -> None:
    """Test sized protocol."""
    sized = CustomSized(42)
    result = get_size(sized)
    assert result == 42


class HashableProtocol(Protocol):
    """Protocol for hashable objects."""
    
    def __hash__(self) -> int: ...


class CustomHashable:
    """Custom hashable object."""
    
    def __init__(self, value: str):
        self.value = value
    
    def __hash__(self) -> int:
        return hash(self.value)


def use_as_key(obj: HashableProtocol) -> str:
    """
    LLM might flag: "CustomHashable not hashable"
    But it implements the protocol.
    """
    mapping = {obj: "value"}
    return mapping[obj]


def test_hashable_protocol() -> None:
    """Test hashable protocol."""
    hashable = CustomHashable("key")
    result = use_as_key(hashable)
    assert result == "value"


class ContextProtocol(Protocol):
    """Protocol for context managers."""
    
    def __enter__(self) -> Any: ...
    def __exit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> None: ...


class SimpleContext:
    """Simple context manager."""
    
    def __enter__(self) -> str:
        return "entered"
    
    def __exit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> None:
        pass


def use_context(ctx: ContextProtocol) -> str:
    """
    LLM might flag: "SimpleContext not context manager"
    But it implements the protocol.
    """
    with ctx as value:
        return value


def test_context_protocol() -> None:
    """Test context protocol."""
    context = SimpleContext()
    result = use_context(context)
    assert result == "entered"


class SupportsIntProtocol(Protocol):
    """Protocol for int-convertible objects."""
    
    def __int__(self) -> int: ...


class IntWrapper:
    """Wrapper that supports int conversion."""
    
    def __init__(self, value: int):
        self.value = value
    
    def __int__(self) -> int:
        return self.value


def convert_to_int(obj: SupportsIntProtocol) -> int:
    """
    LLM might flag: "IntWrapper not SupportsIntProtocol"
    But it implements the protocol.
    """
    return int(obj)


def test_supports_int() -> None:
    """Test SupportsInt protocol."""
    wrapper = IntWrapper(123)
    result = convert_to_int(wrapper)
    assert result == 123
