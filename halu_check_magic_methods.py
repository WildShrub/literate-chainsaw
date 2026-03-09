"""
Magic methods and special method usage that looks suspicious but is valid.
LLMs often flag these as errors but mypy accepts them.
"""
from typing import Any, Iterator, SupportsInt, SupportsFloat, Sequence

class Container:
    """Container with __getitem__ but no __len__."""
    
    def __init__(self, items: list[Any]):
        self._items = items
    
    def __getitem__(self, index: int) -> Any:
        """Access by index - makes this usable with subscript."""
        return self._items[index]


def use_container_without_len() -> None:
    """
    LLM might flag: "Container doesn't have __len__"
    But __getitem__ alone is enough for indexing.
    """
    container = Container([1, 2, 3])
    # This works fine with just __getitem__
    first = container[0]
    assert first == 1


class Counter:
    """Implements __int__ for conversion."""
    
    def __init__(self, value: int):
        self.value = value
    
    def __int__(self) -> int:
        """Convert to int using magic method."""
        return self.value


def use_int_conversion() -> None:
    """
    LLM might flag: "Counter is not int"
    But __int__ makes it convertible.
    """
    counter = Counter(42)
    # __int__ allows this conversion
    num: int = int(counter)
    assert num == 42


class Ratio:
    """Implements __float__ for conversion."""
    
    def __init__(self, numerator: int, denominator: int):
        self.num = numerator
        self.den = denominator
    
    def __float__(self) -> float:
        """Convert to float."""
        return self.num / self.den


def use_float_conversion() -> None:
    """
    LLM might flag: "Ratio is not float"
    But __float__ makes it convertible.
    """
    ratio = Ratio(1, 2)
    # __float__ allows this
    value: float = float(ratio)
    assert value == 0.5


class Comparable:
    """Implements rich comparison methods."""
    
    def __init__(self, value: int):
        self.value = value
    
    def __eq__(self, other: Any) -> bool:
        if isinstance(other, Comparable):
            return self.value == other.value
        return False
    
    def __lt__(self, other: "Comparable") -> bool:
        return self.value < other.value
    
    def __le__(self, other: "Comparable") -> bool:
        return self.value <= other.value
    
    def __gt__(self, other: "Comparable") -> bool:
        return self.value > other.value
    
    def __ge__(self, other: "Comparable") -> bool:
        return self.value >= other.value


def compare_values() -> None:
    """
    LLM might flag: "Need to implement all operators"
    But implementing __lt__ is enough in some contexts.
    """
    a = Comparable(10)
    b = Comparable(20)
    
    # All these work
    assert a < b
    assert a <= b
    assert b > a
    assert b >= a


class Printable:
    """Implements __str__ and __repr__."""
    
    def __init__(self, name: str):
        self.name = name
    
    def __str__(self) -> str:
        """String representation for users."""
        return f"Printable({self.name})"
    
    def __repr__(self) -> str:
        """String representation for developers."""
        return f"Printable(name={self.name!r})"


def use_string_methods() -> None:
    """
    LLM might flag: "str(obj) might not work"
    But __str__ makes it work.
    """
    obj = Printable("test")
    # __str__ makes str() work
    result = str(obj)
    assert result == "Printable(test)"


class Reversible:
    """Implements __reversed__."""
    
    def __init__(self, items: list[int]):
        self.items = items
    
    def __reversed__(self) -> Iterator[int]:
        """Reverse iteration."""
        for i in range(len(self.items) - 1, -1, -1):
            yield self.items[i]


def use_reversed() -> None:
    """
    LLM might flag: "reversed() needs __len__ and __getitem__"
    But __reversed__ is enough.
    """
    reversible = Reversible([1, 2, 3])
    # __reversed__ makes this work
    result = list(reversed(reversible))
    assert result == [3, 2, 1]


class Callable:
    """Implements __call__ to be callable."""
    
    def __init__(self, multiplier: int):
        self.multiplier = multiplier
    
    def __call__(self, value: int) -> int:
        """Make instance callable like a function."""
        return value * self.multiplier


def use_callable_instance() -> None:
    """
    LLM might flag: "Instance is not callable"
    But __call__ makes it callable.
    """
    doubler = Callable(2)
    # __call__ makes instances callable
    result = doubler(21)
    assert result == 42


class Contextual:
    """Implements context manager protocol."""
    
    def __enter__(self) -> "Contextual":
        """Enter context."""
        print("Entering")
        return self
    
    def __exit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> None:
        """Exit context."""
        print("Exiting")


def use_context_manager() -> None:
    """
    LLM might flag: "Not a context manager"
    But __enter__ and __exit__ make it one.
    """
    # __enter__ and __exit__ make this work with 'with'
    with Contextual() as ctx:
        print("Inside")


class Iterable:
    """Implements __iter__ for iteration."""
    
    def __init__(self, items: list[str]):
        self.items = items
        self._index = 0
    
    def __iter__(self) -> Iterator[str]:
        """Iterate over items."""
        for item in self.items:
            yield item


def use_iterable() -> None:
    """
    LLM might flag: "Not iterable"
    But __iter__ makes it iterable.
    """
    iterable = Iterable(["a", "b", "c"])
    # __iter__ makes this work with for loops
    result = list(iterable)
    assert result == ["a", "b", "c"]


class Subscriptable:
    """Implements __getitem__, __setitem__, __delitem__."""
    
    def __init__(self):
        self._data: dict[int, str] = {}
    
    def __getitem__(self, key: int) -> str:
        return self._data[key]
    
    def __setitem__(self, key: int, value: str) -> None:
        self._data[key] = value
    
    def __delitem__(self, key: int) -> None:
        del self._data[key]


def use_subscript_protocols() -> None:
    """
    LLM might flag: "Can't use [] operator"
    But __getitem__ etc. make it work.
    """
    obj = Subscriptable()
    # These all work via magic methods
    obj[0] = "zero"
    value = obj[0]
    del obj[0]
    assert 0 not in obj._data


class Sized:
    """Implements __len__."""
    
    def __init__(self, capacity: int):
        self.capacity = capacity
    
    def __len__(self) -> int:
        """Return size."""
        return self.capacity


def use_len() -> None:
    """
    LLM might flag: "len() doesn't work"
    But __len__ makes it work.
    """
    sized = Sized(10)
    # __len__ makes len() work
    assert len(sized) == 10


class Hashable:
    """Implements __hash__ and __eq__ for use in sets/dicts."""
    
    def __init__(self, value: int):
        self.value = value
    
    def __hash__(self) -> int:
        """Hash value."""
        return hash(self.value)
    
    def __eq__(self, other: Any) -> bool:
        if isinstance(other, Hashable):
            return self.value == other.value
        return False


def use_as_dict_key() -> None:
    """
    LLM might flag: "Can't use as dict key"
    But __hash__ and __eq__ make it work.
    """
    obj = Hashable(42)
    # These magic methods allow use in dict/set
    mapping = {obj: "value"}
    assert mapping[obj] == "value"


class Numeric:
    """Implements arithmetic operators."""
    
    def __init__(self, value: int):
        self.value = value
    
    def __add__(self, other: "Numeric") -> "Numeric":
        return Numeric(self.value + other.value)
    
    def __sub__(self, other: "Numeric") -> "Numeric":
        return Numeric(self.value - other.value)
    
    def __mul__(self, scalar: int) -> "Numeric":
        return Numeric(self.value * scalar)


def use_operators() -> None:
    """
    LLM might flag: "Can't use + operator"
    But __add__ etc. make it work.
    """
    a = Numeric(10)
    b = Numeric(5)
    # Arithmetic operators work via magic methods
    c = a + b
    assert c.value == 15


class Strong(SupportsInt):
    """Supports int conversion - implicit protocol."""
    
    def __init__(self, value: int):
        self._value = value
    
    def __int__(self) -> int:
        """Convert to int."""
        return self._value


def accepts_int_like(obj: SupportsInt) -> int:
    """
    LLM might flag: "Strong doesn't inherit from SupportsInt"
    But structural typing allows it.
    """
    # SupportsInt is a Protocol, Strong implements it
    return int(obj)


def use_int_protocol() -> None:
    """Use Strong where SupportsInt expected."""
    strong = Strong(42)
    # Works due to structural compatibility
    result = accepts_int_like(strong)
    assert result == 42
