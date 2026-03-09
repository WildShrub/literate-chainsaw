"""
TypedDict and Protocol errors - LLMs miss these structural typing mistakes.
"""
from typing import TypedDict, Protocol, List

class UserDict(TypedDict):
    """TypedDict for user data."""
    name: str
    age: int
    email: str


class Animal(Protocol):
    """Protocol defining animal interface."""
    
    def make_sound(self) -> str: ...
    def move(self) -> None: ...


def create_user(name: str, age: int) -> UserDict:
    """Create a user dict."""
    # ERROR: Missing required 'email' key
    return {'name': name, 'age': age}


def add_user_to_list(users: List[UserDict]) -> None:
    """Add user to list."""
    # ERROR: Missing 'email' field
    user: UserDict = {'name': 'Bob', 'age': 25}  # type: ignore
    users.append(user)


def process_user(user: UserDict) -> str:
    """Process user data."""
    # ERROR: TypedDict has no 'phone' field
    return f"{user['name']} - {user['phone']}"


def get_user_dict(name: str, age: int, email: str, **kwargs) -> UserDict:
    """Create user dict from kwargs."""
    # ERROR: Extra fields not allowed in TypedDict
    data: UserDict = {'name': name, 'age': age, 'email': email, 'phone': '555-0000'}
    return data


class Dog:
    """Dog class that partially implements Animal protocol."""
    
    def make_sound(self) -> str:
        return "woof"
    
    # ERROR: Missing 'move' method required by Animal protocol


class Robot:
    """Robot doesn't implement Animal but we try to use it as one."""
    
    def move(self) -> None:
        return None


def use_animal(animal: Animal) -> None:
    """Use any animal."""
    sound = animal.make_sound()
    animal.move()


# ERROR: Dog is missing 'move' method - doesn't fully implement Animal protocol
dog: Animal = Dog()

# ERROR: Robot doesn't implement make_sound - isinstance doesn't work with Protocol, but mypy catches it
robot: Animal = Robot()


class Config(TypedDict, total=False):
    """Partial TypedDict where fields are optional."""
    debug: bool
    timeout: int
    host: str


def get_config() -> Config:
    """Get config."""
    # This is OK for total=False
    return {'debug': True}


def update_config(cfg: Config) -> None:
    """Update config - accessing potentially missing key."""
    # ERROR: 'timeout' might not be in cfg since total=False
    timeout = cfg['timeout']  # mypy warns: key might not exist
    value: int = timeout  # but we assume it's int


class Processor(Protocol):
    """Protocol for processing."""
    
    def process(self, data: str) -> int: ...
    def validate(self) -> bool: ...


class MyProcessor:
    """Implements Processor incorrectly."""
    
    def process(self, data: str) -> str:  # ERROR: should return int, returns str
        return f"Processed: {data}"
    
    def validate(self) -> bool:
        return True


# ERROR: MyProcessor doesn't match Processor protocol (wrong return type)
processor: Processor = MyProcessor()
