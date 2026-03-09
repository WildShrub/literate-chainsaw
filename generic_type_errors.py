"""
Generic type parameter errors - LLMs struggle with TypeVar constraints.
"""
from typing import TypeVar, Generic, List, Dict

T = TypeVar('T', int, str)  # T can only be int or str
U = TypeVar('U')  # U can be anything

class Container(Generic[T]):
    """Generic container that only accepts int or str."""
    
    def __init__(self, value: T):
        self.value = value
    
    def process(self) -> T:
        """Process the value."""
        # ERROR: Can't call .lower() on T because T could be int
        if isinstance(self.value, str):
            return self.value.lower()  # type: ignore - needed because mypy sees Union return
        return self.value


def echo(item: T) -> T:
    """Echo the item back."""
    return item


# ERROR: float violates TypeVar constraint (T = int | str)
result1: Container[float] = Container(3.14)  # mypy error
result2: Container[int] = Container(5)  # OK
result3: Container[str] = Container("hi")  # OK


def combine(a: T, b: U, c: T) -> List[T]:
    """Combine values - c must be same type as a."""
    return [a, c]


# ERROR: c is different type from a - violates constraint
my_list = combine(5, "hello", "world")  # a is int, but c is str


class DataStore(Generic[T]):
    """Stores items of type T."""
    
    def __init__(self):
        self.items: List[T] = []
    
    def add(self, item: T) -> None:
        self.items.append(item)
    
    def get_first(self) -> T:
        return self.items[0]


# ERROR: Creating store typed as int, then adding string
int_store: DataStore[int] = DataStore()
int_store.add(42)  # OK
int_store.add("forty-two")  # ERROR: str is not int


def process_dict(data: Dict[str, T]) -> T:
    """Get value from dict."""
    # ERROR: Could be any key, returns Any if key doesn't exist
    return data['missing_key']  # mypy warns: need to handle KeyError case, type is still T
