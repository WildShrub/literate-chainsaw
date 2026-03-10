"""
Valid magic method implementations that LLMs often incorrectly flag.
These are all valid Python code that mypy accepts.
"""
from typing import Any, Union, Iterator, Iterable, Sized, Container, Callable, Hashable
from abc import ABC, abstractmethod

class Vector:
    """A simple 2D vector with magic methods."""
    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y

    def __add__(self, other: 'Vector') -> 'Vector':
        """Vector addition."""
        return Vector(self.x + other.x, self.y + other.y)

    def __mul__(self, scalar: float) -> 'Vector':
        """Scalar multiplication."""
        return Vector(self.x * scalar, self.y * scalar)

    def __rmul__(self, scalar: float) -> 'Vector':
        """Right scalar multiplication."""
        return self * scalar

    def __str__(self) -> str:
        return f"Vector({self.x}, {self.y})"

    def __repr__(self) -> str:
        return f"Vector({self.x!r}, {self.y!r})"

    def __eq__(self, other: Any) -> bool:
        if isinstance(other, Vector):
            return self.x == other.x and self.y == other.y
        return False

    def __hash__(self) -> int:
        return hash((self.x, self.y))

class Matrix:
    """A simple matrix with magic methods."""
    def __init__(self, data: list):
        self.data = data
        self.rows = len(data)
        self.cols = len(data[0]) if data else 0

    def __getitem__(self, key: tuple) -> float:
        """Matrix indexing."""
        i, j = key
        return self.data[i][j]

    def __setitem__(self, key: tuple, value: float) -> None:
        """Matrix item assignment."""
        i, j = key
        self.data[i][j] = value

    def __len__(self) -> int:
        """Matrix length (number of rows)."""
        return self.rows

    def __iter__(self) -> Iterator[list]:
        """Matrix iteration."""
        return iter(self.data)

class SmartList(list):
    """A list with additional magic methods."""
    def __contains__(self, item: Any) -> bool:
        """Membership test."""
        return super().__contains__(item)

    def __reversed__(self) -> Iterator:
        """Reverse iteration."""
        return reversed(self)

class ConfigDict(dict):
    """A dict that allows attribute access."""
    def __getattr__(self, name: str) -> Any:
        """Attribute access."""
        try:
            return self[name]
        except KeyError:
            raise AttributeError(f"'{type(self).__name__}' has no attribute '{name}'")

    def __setattr__(self, name: str, value: Any) -> None:
        """Attribute assignment."""
        if name.startswith('_'):
            super().__setattr__(name, value)
        else:
            self[name] = value

    def __delattr__(self, name: str) -> None:
        """Attribute deletion."""
        if name.startswith('_'):
            super().__delattr__(name)
        else:
            del self[name]

class LazyProperty:
    """A descriptor for lazy properties."""
    def __init__(self, func: Callable):
        self.func = func
        self.name = func.__name__

    def __get__(self, obj: Any, objtype: Any = None) -> Any:
        if obj is None:
            return self
        value = self.func(obj)
        setattr(obj, self.name, value)
        return value

class CallableClass:
    """A class that can be called like a function."""
    def __init__(self, multiplier: int):
        self.multiplier = multiplier

    def __call__(self, x: int) -> int:
        """Make the class callable."""
        return x * self.multiplier

class ContextManager:
    """A simple context manager."""
    def __enter__(self) -> 'ContextManager':
        print("Entering context")
        return self

    def __exit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> None:
        print("Exiting context")
        return None

class NumberLike:
    """A number-like class with comparison magic methods."""
    def __init__(self, value: float):
        self.value = value

    def __lt__(self, other: 'NumberLike') -> bool:
        return self.value < other.value

    def __le__(self, other: 'NumberLike') -> bool:
        return self.value <= other.value

    def __gt__(self, other: 'NumberLike') -> bool:
        return self.value > other.value

    def __ge__(self, other: 'NumberLike') -> bool:
        return self.value >= other.value

    def __eq__(self, other: Any) -> bool:
        if isinstance(other, NumberLike):
            return self.value == other.value
        return False

    def __ne__(self, other: Any) -> bool:
        return not self.__eq__(other)

class Subscriptable:
    """A class that supports advanced subscripting."""
    def __init__(self, data: dict):
        self.data = data

    def __getitem__(self, key: Union[str, int, slice]) -> Any:
        """Advanced getitem."""
        if isinstance(key, str):
            return self.data.get(key, "not found")
        elif isinstance(key, int):
            keys = list(self.data.keys())
            return self.data[keys[key]]
        elif isinstance(key, slice):
            items = list(self.data.items())
            return dict(items[key])
        else:
            raise TypeError("Invalid key type")

    def __setitem__(self, key: Union[str, int], value: Any) -> None:
        """Advanced setitem."""
        if isinstance(key, str):
            self.data[key] = value
        elif isinstance(key, int):
            keys = list(self.data.keys())
            self.data[keys[key]] = value
        else:
            raise TypeError("Invalid key type")

    def __delitem__(self, key: Union[str, int]) -> None:
        """Advanced delitem."""
        if isinstance(key, str):
            del self.data[key]
        elif isinstance(key, int):
            keys = list(self.data.keys())
            del self.data[keys[key]]
        else:
            raise TypeError("Invalid key type")

class Arithmetic:
    """A class with arithmetic magic methods."""
    def __init__(self, value: int):
        self.value = value

    def __add__(self, other: Union['Arithmetic', int]) -> 'Arithmetic':
        if isinstance(other, Arithmetic):
            return Arithmetic(self.value + other.value)
        return Arithmetic(self.value + other)

    def __radd__(self, other: int) -> 'Arithmetic':
        return Arithmetic(other + self.value)

    def __iadd__(self, other: Union['Arithmetic', int]) -> 'Arithmetic':
        if isinstance(other, Arithmetic):
            self.value += other.value
        else:
            self.value += other
        return self

    def __sub__(self, other: Union['Arithmetic', int]) -> 'Arithmetic':
        if isinstance(other, Arithmetic):
            return Arithmetic(self.value - other.value)
        return Arithmetic(self.value - other)

    def __neg__(self) -> 'Arithmetic':
        return Arithmetic(-self.value)

    def __pos__(self) -> 'Arithmetic':
        return Arithmetic(+self.value)

    def __abs__(self) -> 'Arithmetic':
        return Arithmetic(abs(self.value))

class StringWrapper:
    """A string wrapper with string magic methods."""
    def __init__(self, text: str):
        self.text = text

    def __str__(self) -> str:
        return self.text

    def __repr__(self) -> str:
        return f"StringWrapper({self.text!r})"

    def __len__(self) -> int:
        return len(self.text)

    def __getitem__(self, key: Union[int, slice]) -> Union[str, 'StringWrapper']:
        result = self.text[key]
        if isinstance(result, str):
            return StringWrapper(result)
        return result

    def __add__(self, other: Union[str, 'StringWrapper']) -> 'StringWrapper':
        if isinstance(other, StringWrapper):
            return StringWrapper(self.text + other.text)
        return StringWrapper(self.text + other)

    def __radd__(self, other: str) -> 'StringWrapper':
        return StringWrapper(other + self.text)

    def __mul__(self, n: int) -> 'StringWrapper':
        return StringWrapper(self.text * n)

    def __rmul__(self, n: int) -> 'StringWrapper':
        return StringWrapper(self.text * n)

    def __contains__(self, item: str) -> bool:
        return item in self.text

class Descriptor:
    """A simple descriptor."""
    def __init__(self, name: str):
        self.name = name

    def __get__(self, obj: Any, objtype: Any = None) -> Any:
        if obj is None:
            return self
        return getattr(obj, f"_{self.name}", None)

    def __set__(self, obj: Any, value: Any) -> None:
        setattr(obj, f"_{self.name}", value)

    def __delete__(self, obj: Any) -> None:
        delattr(obj, f"_{self.name}")

class MetaClass(type):
    """A simple metaclass."""
    def __new__(cls, name: str, bases: tuple, namespace: dict) -> type:
        # Add a class attribute
        namespace['created_by_metaclass'] = True
        return super().__new__(cls, name, bases, namespace)

    def __init__(cls, name: str, bases: tuple, namespace: dict) -> None:
        super().__init__(name, bases, namespace)
        cls.metaclass_initialized = True

class MetaClassExample(metaclass=MetaClass):
    """A class using the metaclass."""
    pass

class IteratorExample:
    """A simple iterator."""
    def __init__(self, items: list):
        self.items = items
        self.index = 0

    def __iter__(self) -> 'IteratorExample':
        return self

    def __next__(self) -> Any:
        if self.index >= len(self.items):
            raise StopIteration
        value = self.items[self.index]
        self.index += 1
        return value

class GeneratorWrapper:
    """A wrapper that makes any iterable a generator."""
    def __init__(self, iterable: Iterable):
        self.iterable = iterable

    def __iter__(self) -> Iterator:
        return iter(self.iterable)

class BoolLike:
    """A class with truthiness magic methods."""
    def __init__(self, value: bool):
        self.value = value

    def __bool__(self) -> bool:
        return self.value

class HashableClass:
    """A hashable class."""
    def __init__(self, value: Any):
        self.value = value

    def __hash__(self) -> int:
        return hash(self.value)

    def __eq__(self, other: Any) -> bool:
        if isinstance(other, HashableClass):
            return self.value == other.value
        return False

class Comparable:
    """A comparable class."""
    def __init__(self, value: Any):
        self.value = value

    def __lt__(self, other: 'Comparable') -> bool:
        return self.value < other.value

    def __le__(self, other: 'Comparable') -> bool:
        return self.value <= other.value

    def __gt__(self, other: 'Comparable') -> bool:
        return self.value > other.value

    def __ge__(self, other: 'Comparable') -> bool:
        return self.value >= other.value

class SizedClass:
    """A sized class."""
    def __init__(self, size: int):
        self.size = size

    def __len__(self) -> int:
        return self.size

class ContainerClass:
    """A container class."""
    def __init__(self, items: list):
        self.items = items

    def __contains__(self, item: Any) -> bool:
        return item in self.items

class CallableDescriptor:
    """A callable descriptor."""
    def __init__(self, func: Callable):
        self.func = func

    def __get__(self, obj: Any, objtype: Any = None) -> Callable:
        if obj is None:
            return self
        return lambda *args, **kwargs: self.func(obj, *args, **kwargs)

    def __call__(self, *args, **kwargs) -> Any:
        return self.func(*args, **kwargs)