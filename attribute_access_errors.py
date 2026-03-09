"""
Attribute access and inheritance errors - mypy catches what LLMs might miss.
"""
from typing import Any, cast

class Base:
    """Base class."""
    name: str
    
    def __init__(self, name: str):
        self.name = name
    
    def describe(self) -> str:
        return f"Base: {self.name}"


class Derived(Base):
    """Derived class."""
    age: int
    
    def __init__(self, name: str, age: int):
        super().__init__(name)
        self.age = age


def access_attributes() -> None:
    """Access attributes that may not exist."""
    base: Base = Base("test")
    
    # OK: name is in Base
    print(base.name)
    
    # ERROR: age is not in Base class
    print(base.age)


def polymorphic_access(obj: Base) -> str:
    """Access derived-only attributes on base type."""
    # ERROR: age doesn't exist on Base, only on Derived
    return f"Age: {obj.age}"


class Person:
    """Person without age attribute initially."""
    
    def __init__(self, name: str):
        self.name = name
        # Deliberately not setting age here
    
    def get_info(self) -> str:
        # ERROR: age is not guaranteed to exist (not set in __init__)
        return f"{self.name} is {self.age}"


class Config:
    """Config with optional attributes."""
    
    def __init__(self, debug: bool = False):
        self.debug = debug
        # age and name are not set
    
    def get_all_fields(self) -> dict[str, Any]:
        # ERROR: These attributes don't exist
        return {
            'debug': self.debug,
            'name': self.name,  # doesn't exist
            'age': self.age      # doesn't exist
        }


def access_dict_attrs() -> None:
    """Access attributes on dict."""
    data = {'key': 'value'}
    
    # ERROR: dict doesn't have an 'items' attribute... wait, it does
    # But ERROR: dict doesn't have a 'shuffle' method
    items = data.shuffle()  # type: ignore


def chain_access() -> None:
    """Chain attribute access."""
    base = Base("test")
    
    # OK: describe returns str, which has upper
    result = base.describe().upper()
    
    # ERROR: describe returns str, str doesn't have write method
    base.describe().write("file.txt")


class Widget:
    """Widget class."""
    
    def render(self) -> str:
        return "<div></div>"
    
    def set_color(self, color: str) -> None:
        self.color = color


def widget_chain() -> None:
    """Chain method calls."""
    widget = Widget()
    
    # ERROR: render() returns str, which doesn't have set_color method
    result = widget.render().set_color("red")


class Parent:
    """Parent class."""
    
    def method(self) -> str:
        return "parent"


class Child(Parent):
    """Child class."""
    
    def method(self) -> int:  # ERROR: Changes return type - breaks Liskov principle
        return 42
    
    def child_only(self) -> str:
        return "child"


def use_parent(p: Parent) -> None:
    """Use parent type."""
    result = p.method()
    # mypy thinks result is str from Parent.method
    # but if p is actually Child, result would be int
    upper = result.upper()  # Safe according to mypy, but could fail at runtime


def process_derived(p: Parent) -> None:
    """Process derived class."""
    # ERROR: child_only doesn't exist on Parent type
    p.child_only()


class Untyped:
    """Class without type annotations."""
    
    def __init__(self, x):  # No type hint
        self.value = x


def access_untyped() -> None:
    """Access on untyped object."""
    obj = Untyped(42)
    
    # mypy may allow this depending on settings, but it's risky
    result = obj.value + 10  # value could be anything


class Annotated:
    """Class with proper annotations."""
    value: int
    
    def __init__(self, x: int):
        self.value = x


def use_any_cast(value: Any) -> int:
    """Using cast to bypass type checking."""
    # Using cast tells mypy "trust me, this is int"
    # but it could be anything at runtime
    number = cast(int, value)
    return number * 2


def risky_cast() -> int:
    """Dangerous cast that mypy won't catch."""
    data = "not a number"
    number = cast(int, data)  # mypy believes this is int
    return number + 10  # Runtime ERROR: can't add int + str


class Generic:
    """Class with generic attributes."""
    
    items: list  # No type parameter
    
    def __init__(self):
        self.items = []
    
    def add(self, item) -> None:  # No type hint
        self.items.append(item)
    
    def get_first(self) -> int:  # Claims to return int
        return self.items[0]  # But could return anything


def test_generic() -> None:
    """Test generic class."""
    gen = Generic()
    gen.add("string")
    result = gen.get_first()  # mypy thinks it's int
    print(result + 10)  # Would fail at runtime since result is "string"
