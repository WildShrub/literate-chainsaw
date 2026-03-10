"""
Duck typing and structural subtyping examples that LLMs often flag incorrectly.
These are all valid Python code that mypy accepts.
"""
from typing import Protocol, Any, Union, runtime_checkable
from abc import ABC, abstractmethod

@runtime_checkable
class HasUpper(Protocol):
    """Protocol for objects with upper method."""
    def upper(self) -> str: ...

@runtime_checkable
class HasLen(Protocol):
    """Protocol for objects with len."""
    def __len__(self) -> int: ...

@runtime_checkable
class Drawable(Protocol):
    """Protocol for drawable objects."""
    def draw(self, canvas: Any) -> None: ...

@runtime_checkable
class IterableProtocol(Protocol):
    """Protocol for iterable objects."""
    def __iter__(self): ...

@runtime_checkable
class SizedProtocol(Protocol):
    """Protocol for sized objects."""
    def __len__(self) -> int: ...

class StringWrapper:
    """A class that behaves like a string."""
    def __init__(self, value: str):
        self.value = value

    def upper(self) -> str:
        return self.value.upper()

    def __str__(self) -> str:
        return self.value

class ListWrapper:
    """A class that behaves like a list."""
    def __init__(self, items):
        self.items = list(items)

    def __len__(self) -> int:
        return len(self.items)

    def __iter__(self):
        return iter(self.items)

def process_text(obj: HasUpper) -> str:
    """Process any object that has an upper method."""
    return obj.upper()

def get_length(obj: HasLen) -> int:
    """Get length of any object that has __len__."""
    return len(obj)

def draw_shapes(shapes: list[Drawable], canvas: Any) -> None:
    """Draw any objects that have a draw method."""
    for shape in shapes:
        shape.draw(canvas)

def sum_lengths(items: list[HasLen]) -> int:
    """Sum lengths of objects that have __len__."""
    return sum(len(item) for item in items)

def iterate_over(obj: IterableProtocol) -> list:
    """Iterate over any object that has __iter__."""
    return list(obj)

def check_size(obj: Union[HasLen, SizedProtocol]) -> int:
    """Check size using either protocol."""
    return len(obj)

# Duck typing examples
def duck_upper(obj: Any) -> str:
    """Duck typing - if it has upper, use it."""
    if hasattr(obj, 'upper'):
        return obj.upper()
    return str(obj)

def duck_len(obj: Any) -> int:
    """Duck typing - if it has len, use it."""
    if hasattr(obj, '__len__'):
        return len(obj)
    return 0

def duck_iter(obj: Any) -> list:
    """Duck typing - if it has iter, use it."""
    try:
        return list(obj)
    except TypeError:
        return []

# Structural subtyping examples
class FileLike:
    """A file-like object."""
    def read(self, size: int = -1) -> str:
        return "data"

    def close(self) -> None:
        pass

@runtime_checkable
class FileProtocol(Protocol):
    """Protocol for file-like objects."""
    def read(self, size: int = -1) -> str: ...
    def close(self) -> None: ...

def read_file(file: FileProtocol) -> str:
    """Read from any file-like object."""
    try:
        return file.read()
    finally:
        file.close()

# Generic protocols
@runtime_checkable
class Comparable(Protocol):
    """Protocol for comparable objects."""
    def __lt__(self, other: Any) -> bool: ...
    def __gt__(self, other: Any) -> bool: ...

def find_max(items: list[Comparable]) -> Comparable:
    """Find maximum in list of comparables."""
    if not items:
        raise ValueError("Empty list")
    max_item = items[0]
    for item in items:
        if item > max_item:
            max_item = item
    return max_item

# Protocol inheritance
@runtime_checkable
class Readable(Protocol):
    """Basic readable protocol."""
    def read(self) -> str: ...

@runtime_checkable
class Writable(Protocol):
    """Basic writable protocol."""
    def write(self, data: str) -> None: ...

@runtime_checkable
class ReadWritable(Readable, Writable, Protocol):
    """Combined read/write protocol."""
    pass

class Buffer:
    """A buffer that can read and write."""
    def __init__(self):
        self.data = ""

    def read(self) -> str:
        return self.data

    def write(self, data: str) -> None:
        self.data += data

def process_buffer(buf: ReadWritable) -> str:
    """Process a read-writable buffer."""
    buf.write("hello")
    return buf.read()

# Duck typing with magic methods
class NumberLike:
    """A number-like object."""
    def __init__(self, value: float):
        self.value = value

    def __add__(self, other):
        if hasattr(other, 'value'):
            return NumberLike(self.value + other.value)
        return NumberLike(self.value + other)

    def __str__(self):
        return str(self.value)

def add_numbers(a: Any, b: Any) -> Any:
    """Add any number-like objects."""
    return a + b

# Protocol with optional methods
@runtime_checkable
class OptionalCloseable(Protocol):
    """Protocol with optional close method."""
    def close(self) -> None: ...

def safe_close(obj: Any) -> None:
    """Close object if it has a close method."""
    if hasattr(obj, 'close'):
        obj.close()

# Structural typing with callables
@runtime_checkable
class CallableProtocol(Protocol):
    """Protocol for callable objects."""
    def __call__(self, x: int) -> int: ...

def apply_func(func: CallableProtocol, value: int) -> int:
    """Apply a callable that takes int and returns int."""
    return func(value)

# Duck typing with attributes
class Config:
    """A configuration object."""
    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v)

def get_config_value(config: Any, key: str, default: Any = None) -> Any:
    """Get config value using duck typing."""
    return getattr(config, key, default)

# Protocol with generic types
from typing import TypeVar, Generic

T = TypeVar('T')
T_contra = TypeVar('T_contra', contravariant=True)

@runtime_checkable
class Container(Protocol, Generic[T_contra]):
    """Protocol for containers."""
    def __contains__(self, item: T_contra) -> bool: ...

def check_membership(container: Container[str], item: str) -> bool:
    """Check if item is in container."""
    return item in container