"""
Duck typing and structural subtyping that work without inheritance.
LLMs often flag these as errors, but they're valid in Python typing.
"""
from typing import Protocol, Any, Iterator, Generic, TypeVar, List

class Drawable(Protocol):
    """Protocol for drawable objects."""
    
    def draw(self) -> str: ...


class Circle:
    """Circle implements Drawable without inheriting from it."""
    
    def draw(self) -> str:
        return "●"


class Square:
    """Square also implements Drawable implicitly."""
    
    def draw(self) -> str:
        return "■"


def render_shape(shape: Drawable) -> str:
    """Function that accepts anything drawable."""
    # LLM might flag: "Circle isn't a Drawable"
    # But Python's structural typing allows it
    return f"Drawing: {shape.draw()}"


def use_protocol_correctly() -> None:
    """Use shapes with protocol typing."""
    circle = Circle()
    square = Square()
    
    # Both work even though they don't explicitly inherit from Drawable
    print(render_shape(circle))
    print(render_shape(square))


class Iterable_(Protocol):
    """Custom iterable protocol."""
    
    def __iter__(self) -> Iterator[int]: ...


class CountUp:
    """Custom iterable that works with Iterable_ protocol."""
    
    def __init__(self, max_val: int):
        self.max_val = max_val
    
    def __iter__(self) -> Iterator[int]:
        for i in range(self.max_val):
            yield i


def sum_iterable(values: Iterable_) -> int:
    """Sum any iterable."""
    # LLM might worry about CountUp
    # But it has __iter__, so it structurally matches
    total = 0
    for val in values:
        total += val
    return total


def use_custom_iterable() -> None:
    """Use custom iterable."""
    counter = CountUp(5)
    result = sum_iterable(counter)  # Works perfectly
    assert result == 10


class SizedContainer(Protocol):
    """Protocol for sized containers."""
    
    def __len__(self) -> int: ...


class CustomList:
    """Custom container implementing __len__."""
    
    def __init__(self, items: List[Any]):
        self.items = items
    
    def __len__(self) -> int:
        return len(self.items)


def get_size(container: SizedContainer) -> int:
    """Get size of any sized container."""
    # LLM might flag: CustomList doesn't inherit from SizedContainer
    # But it has __len__, so it matches the protocol
    return len(container)


def use_sized_container() -> None:
    """Use custom container."""
    my_list = CustomList([1, 2, 3])
    size = get_size(my_list)
    assert size == 3


class Comparable(Protocol):
    """Protocol for comparable objects."""
    
    def __lt__(self, other: Any) -> bool: ...
    def __eq__(self, other: Any) -> bool: ...


class Version:
    """Version that implements comparison operators."""
    
    def __init__(self, major: int, minor: int):
        self.major = major
        self.minor = minor
    
    def __lt__(self, other: "Version") -> bool:
        if self.major != other.major:
            return self.major < other.major
        return self.minor < other.minor
    
    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Version):
            return False
        return self.major == other.major and self.minor == other.minor


def min_version(v1: Comparable, v2: Comparable) -> Comparable:
    """Get minimum of two comparable objects."""
    # Works with Version even though it doesn't inherit from Comparable
    return v1 if v1 < v2 else v2


T = TypeVar('T')

class Container(Protocol[T]):
    """Generic protocol for containers."""
    
    def __getitem__(self, index: int) -> T: ...


class SimpleList(Generic[T]):
    """Simple list that implements Container protocol."""
    
    def __init__(self, items: List[T]):
        self.items = items
    
    def __getitem__(self, index: int) -> T:
        return self.items[index]


def get_first(container: Container[T]) -> T:
    """Get first item from any container."""
    # Works with SimpleList even without explicit inheritance
    return container[0]


def use_generic_protocol() -> None:
    """Use generic protocol."""
    int_list = SimpleList([1, 2, 3])
    first: int = get_first(int_list)
    assert first == 1


class Callable_(Protocol):
    """Protocol for callable objects."""
    
    def __call__(self, x: int) -> str: ...


class Formatter:
    """Formatter that acts like a callable."""
    
    def __call__(self, x: int) -> str:
        return f"Value: {x}"


def apply_formatter(formatter: Callable_, value: int) -> str:
    """Apply any formatter."""
    # Formatter matches Callable_ protocol structurally
    return formatter(value)


def use_callable_protocol() -> None:
    """Use callable protocol."""
    fmt = Formatter()
    result = apply_formatter(fmt, 42)
    assert result == "Value: 42"


class FileWriter(Protocol):
    """Protocol for file writers."""
    
    def write(self, data: str) -> None: ...
    def close(self) -> None: ...


class StringWriter:
    """Writer that stores to string."""
    
    def __init__(self):
        self.content = ""
    
    def write(self, data: str) -> None:
        self.content += data
    
    def close(self) -> None:
        pass


def write_to_file(writer: FileWriter, message: str) -> None:
    """Write using any file writer."""
    # StringWriter matches FileWriter protocol
    writer.write(message)
    writer.close()


def use_file_protocol() -> None:
    """Use file protocol."""
    writer = StringWriter()
    write_to_file(writer, "Hello")


class Context(Protocol):
    """Protocol for context managers."""
    
    def __enter__(self) -> "Context": ...
    def __exit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> None: ...


class MyContext:
    """Context manager without explicit inheritance."""
    
    def __enter__(self) -> "MyContext":
        return self
    
    def __exit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> None:
        pass


def use_context(ctx: Context) -> None:
    """Use any context manager."""
    # MyContext matches Context protocol
    with ctx:
        pass
