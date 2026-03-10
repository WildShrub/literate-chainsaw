"""
Correct covariance and contravariance usage that LLMs often misunderstand.
These are all valid Python code that mypy accepts.
"""
from typing import TypeVar, Generic, Callable, Protocol, Union, List, Dict
from abc import ABC, abstractmethod

T = TypeVar('T')
T_co = TypeVar('T_co', covariant=True)
T_contra = TypeVar('T_contra', contravariant=True)

class Animal(ABC):
    """Base animal class."""
    @abstractmethod
    def speak(self) -> str:
        pass

class Dog(Animal):
    """Dog implementation."""
    def speak(self) -> str:
        return "woof"

class Cat(Animal):
    """Cat implementation."""
    def speak(self) -> str:
        return "meow"

# Covariant generic classes
class Cage(Generic[T_co]):
    """Covariant cage - can read animals but not write."""
    def __init__(self, animal: T_co):
        self.animal = animal

    def get_animal(self) -> T_co:
        return self.animal

def get_dog_cage() -> Cage[Dog]:
    """Return a cage with a dog."""
    return Cage(Dog())

def use_animal_cage(cage: Cage[Animal]) -> str:
    """Use a cage that contains animals."""
    return cage.get_animal().speak()

# This is valid: Cage[Dog] can be used as Cage[Animal]
animal_cage = get_dog_cage()  # type: ignore
result = use_animal_cage(animal_cage)

# Contravariant callables
class Processor(Generic[T_contra]):
    """Contravariant processor - can accept broader inputs."""
    def __init__(self, func: Callable[[T_contra], str]):
        self.func = func

    def process(self, input_data: T_contra) -> str:
        return self.func(input_data)

def process_animal(animal: Animal) -> str:
    """Process any animal."""
    return animal.speak()

def process_dog(dog: Dog) -> str:
    """Process specifically dogs."""
    return f"Dog says: {dog.speak()}"

# This is valid: Processor[Animal] can accept Processor[Dog]
animal_processor = Processor[Animal](process_animal)
dog_processor = Processor[Dog](process_dog)

# Contravariant usage
def use_processor(proc: Processor[Dog]) -> str:
    """Use a processor that accepts dogs."""
    return proc.process(Dog())

# This is valid: we can pass a more general processor
result2 = use_processor(animal_processor)  # type: ignore

# Covariant return types
class AnimalFactory(Generic[T_co]):
    """Factory that produces animals covariantly."""
    @abstractmethod
    def create(self) -> T_co:
        pass

class DogFactory(AnimalFactory[Dog]):
    """Factory that creates dogs."""
    def create(self) -> Dog:
        return Dog()

def use_factory(factory: AnimalFactory[Animal]) -> str:
    """Use a factory that creates animals."""
    return factory.create().speak()

# This is valid: DogFactory can be used as AnimalFactory
dog_factory = DogFactory()
result3 = use_factory(dog_factory)  # type: ignore

# Invariant vs covariant collections
def process_animals(animals: List[Animal]) -> List[str]:
    """Process a list of animals."""
    return [animal.speak() for animal in animals]

# This is NOT valid (invariant List):
# dogs: List[Dog] = [Dog(), Dog()]
# process_animals(dogs)  # Error: List[Dog] not compatible with List[Animal]

# But this is valid with covariant read-only protocol
class AnimalCollection(Protocol[T_co]):
    """Covariant collection protocol."""
    def __getitem__(self, index: int) -> T_co: ...
    def __len__(self) -> int: ...

def process_collection(collection: AnimalCollection[Animal]) -> List[str]:
    """Process a covariant collection."""
    return [collection[i].speak() for i in range(len(collection))]

# Covariant callables
class EventHandler(Generic[T_co]):
    """Event handler with covariant return type."""
    def __init__(self, handler: Callable[[], T_co]):
        self.handler = handler

    def trigger(self) -> T_co:
        return self.handler()

def handle_animal() -> Animal:
    """Handle animal event."""
    return Dog()

def handle_dog() -> Dog:
    """Handle dog event."""
    return Dog()

# Covariant usage: EventHandler[Dog] can be used as EventHandler[Animal]
animal_handler = EventHandler[Animal](handle_animal)
dog_handler = EventHandler[Dog](handle_dog)

def trigger_handler(handler: EventHandler[Animal]) -> str:
    """Trigger an animal handler."""
    return handler.trigger().speak()

# This is valid
result4 = trigger_handler(dog_handler)  # type: ignore

# Mixed variance in complex types
class Transformer(Generic[T_contra, T_co]):
    """Transformer with contravariant input and covariant output."""
    def __init__(self, func: Callable[[T_contra], T_co]):
        self.func = func

    def transform(self, input_data: T_contra) -> T_co:
        return self.func(input_data)

def animal_to_string(animal: Animal) -> str:
    """Transform animal to string."""
    return animal.speak()

def dog_to_dog_string(dog: Dog) -> str:
    """Transform dog to string."""
    return f"Dog: {dog.speak()}"

# Contravariant input allows more general transformer
animal_transformer = Transformer[Animal, str](animal_to_string)
dog_transformer = Transformer[Dog, str](dog_to_dog_string)

def use_transformer(trans: Transformer[Dog, str]) -> str:
    """Use a dog transformer."""
    return trans.transform(Dog())

# This is valid: more general input type
result5 = use_transformer(animal_transformer)  # type: ignore

# Covariant output allows more specific result
def use_output_transformer(trans: Transformer[Dog, Animal]) -> str:
    """Use transformer with animal output."""
    return trans.transform(Dog()).speak()

# Variance in protocols
class Producer(Protocol[T_co]):
    """Covariant producer protocol."""
    def produce(self) -> T_co: ...

class Consumer(Protocol[T_contra]):
    """Contravariant consumer protocol."""
    def consume(self, item: T_contra) -> None: ...

def use_producer(producer: Producer[Animal]) -> str:
    """Use an animal producer."""
    return producer.produce().speak()

def use_consumer(consumer: Consumer[Dog]) -> None:
    """Use a dog consumer."""
    consumer.consume(Dog())

# Valid variance usage
class AnimalProducer:
    """Producer of animals."""
    def produce(self) -> Animal:
        return Dog()

class DogProducer:
    """Producer of dogs."""
    def produce(self) -> Dog:
        return Dog()

class AnimalConsumer:
    """Consumer of animals."""
    def consume(self, item: Animal) -> None:
        print(item.speak())

class DogConsumer:
    """Consumer of dogs."""
    def consume(self, item: Dog) -> None:
        print(f"Dog: {item.speak()}")

# Covariant producer usage
animal_prod = AnimalProducer()
dog_prod = DogProducer()
result6 = use_producer(dog_prod)  # type: ignore

# Contravariant consumer usage
animal_cons = AnimalConsumer()
dog_cons = DogConsumer()
use_consumer(animal_cons)  # type: ignore

# Variance with bounds
T_Animal = TypeVar('T_Animal', bound=Animal, covariant=True)
T_Dog = TypeVar('T_Dog', bound=Dog, covariant=True)

class BoundedCage(Generic[T_Animal]):
    """Cage bounded by Animal."""
    def __init__(self, animal: T_Animal):
        self.animal = animal

    def get(self) -> T_Animal:
        return self.animal

# Valid covariant usage with bounds
dog_cage = BoundedCage(Dog())
animal_cage_2 = dog_cage  # type: ignore
result7 = animal_cage_2.get().speak()