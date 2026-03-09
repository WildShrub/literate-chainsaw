"""
Callable and function signature errors - subtle issues LLMs often miss.
"""
from typing import Callable, List, Optional

# Function type signatures that look similar but aren't compatible

def simple_function(x: int) -> str:
    """Simple function converting int to str."""
    return str(x)


def another_function(x: str) -> str:
    """Different signature."""
    return x.upper()


def apply_operation(func: Callable[[int], str], value: int) -> str:
    """Apply a function to a value."""
    return func(value)


def chain_operations() -> None:
    """Chain operations with wrong signatures."""
    # ERROR: another_function expects str, but apply_operation requires Callable[[int], str]
    result = apply_operation(another_function, 42)


def process_list(items: List[int], transformer: Callable[[int], int]) -> List[int]:
    """Process list with transformer function."""
    return [transformer(item) for item in items]


def double(x: int) -> int:
    """Double a number."""
    return x * 2


def stringify(x: int) -> str:
    """Convert to string."""
    return str(x)


def test_callbacks() -> None:
    """Test callback signatures."""
    numbers = [1, 2, 3]
    
    # OK: double has signature Callable[[int], int]
    doubled = process_list(numbers, double)
    
    # ERROR: stringify has signature Callable[[int], str], not Callable[[int], int]
    stringified = process_list(numbers, stringify)


Callback = Callable[[int, str], None]  # Takes int and str


def register_callback(handler: Callback) -> None:
    """Register a callback handler."""
    handler(42, "test")


def single_arg_handler(x: int) -> None:
    """Handler with wrong signature - missing str parameter."""
    print(f"Got: {x}")


# ERROR: single_arg_handler doesn't match Callback signature (missing str parameter)
register_callback(single_arg_handler)


OptionalFunc = Optional[Callable[[int], str]]


def maybe_apply(func: OptionalFunc, value: int) -> Optional[str]:
    """Maybe apply a function."""
    if func is not None:
        return func(value)
    return None


def test_optional_func() -> None:
    """Test optional function."""
    # ERROR: Callable[[int], int] not compatible with Callable[[int], str]
    func: OptionalFunc = lambda x: x * 2  # Wrong return type


def filter_with_predicate(
    items: List[int],
    predicate: Callable[[int], bool]
) -> List[int]:
    """Filter items with a predicate."""
    return [item for item in items if predicate(item)]


def is_even(x: int) -> bool:
    """Check if even."""
    return x % 2 == 0


def format_number(x: int) -> str:
    """Format number."""
    return f"#{x}"


def test_predicate() -> None:
    """Test predicate."""
    numbers = [1, 2, 3, 4]
    
    # OK: is_even has correct signature
    evens = filter_with_predicate(numbers, is_even)
    
    # ERROR: format_number returns str, not bool
    formatted = filter_with_predicate(numbers, format_number)


# Variance issues with callable return types
def get_int_or_str() -> int | str:
    """Return int or str."""
    return 42


def get_int() -> int:
    """Return int."""
    return 42


# ERROR: These look similar but aren't compatible
func1: Callable[[], int | str] = get_int  # Covariance: int is subtype of int|str, so OK
func2: Callable[[], int] = get_int_or_str  # ERROR: int|str is not a subtype of int


def call_func(f: Callable[[], int]) -> int:
    """Call a function that returns int."""
    return f()


# ERROR: get_int_or_str returns int|str, but call_func expects Callable that returns int
result = call_func(get_int_or_str)
