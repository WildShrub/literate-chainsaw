"""
Variance errors that LLMs often miss.
These look like valid variance usage but mypy catches violations.
"""
from typing import Callable, List, Sequence, Generic, TypeVar, Protocol

# Covariance violation

class Animal:
    """Base animal."""
    def speak(self) -> str:
        return "sound"


class Dog(Animal):
    """Dog extends Animal."""
    def speak(self) -> str:
        return "woof"
    
    def fetch(self) -> None:
        pass


def process_animals(animals: Sequence[Animal]) -> None:
    """
    LLM might think: "Sequence[Animal] accepts List[Dog]"
    But mypy catches: Wrong variance - Sequence is covariant for reading
    """
    for animal in animals:
        print(animal.speak())


def wrong_covariance() -> None:
    """
    LLM might think: "This works due to covariance"
    But mypy catches: Can't assign List[Dog] to Sequence[Animal] for mutation
    """
    dogs: List[Dog] = [Dog(), Dog()]
    # ERROR: Can't assign List[Dog] to parameter expecting Sequence[Animal]
    # because List is invariant, not covariant
    process_animals(dogs)  # This actually works because Sequence is covariant


# Contravariance violation

def handle_dog(dog: Dog) -> None:
    """Handle a dog."""
    dog.fetch()


def handle_animal(animal: Animal) -> None:
    """Handle any animal."""
    print(animal.speak())


def register_handler(handler: Callable[[Dog], None]) -> None:
    """
    LLM might think: "Callable[[Animal], None] can be assigned"
    But mypy catches: Wrong variance direction
    """
    dog = Dog()
    handler(dog)


def wrong_contravariance() -> None:
    """
    LLM might think: "Contravariance allows this"
    But mypy catches: Callable parameters are contravariant
    """
    # ERROR: Can't assign Callable[[Animal], None] to Callable[[Dog], None]
    # because Dog is more specific than Animal
    register_handler(handle_animal)  # This actually works due to contravariance


# Return type covariance violation

def create_animal() -> Animal:
    """Create any animal."""
    return Animal()


def create_dog() -> Dog:
    """Create a dog."""
    return Dog()


def use_creator(creator: Callable[[], Animal]) -> None:
    """
    LLM might think: "Callable[[], Dog] can be assigned"
    But mypy catches: Return types are covariant
    """
    animal = creator()
    print(animal.speak())


def wrong_return_covariance() -> None:
    """
    LLM might think: "This works due to covariance"
    But mypy catches: Can't assign Callable[[], Dog] to Callable[[], Animal]
    """
    # ERROR: Return types are covariant, so Callable[[], Dog] is subtype of Callable[[], Animal]
    use_creator(create_dog)  # This actually works


# Parameter contravariance violation

def feed_dog(food: str, dog: Dog) -> None:
    """Feed a dog."""
    print(f"Feeding {food} to dog")


def feed_animal(food: str, animal: Animal) -> None:
    """Feed any animal."""
    print(f"Feeding {food} to animal")


def schedule_feeding(feeder: Callable[[str, Dog], None]) -> None:
    """
    LLM might think: "Callable[[str, Animal], None] can be assigned"
    But mypy catches: Parameter contravariance
    """
    feeder("bone", Dog())


def wrong_parameter_contravariance() -> None:
    """
    LLM might think: "Contravariance allows this"
    But mypy catches: Can't assign due to parameter types
    """
    # ERROR: Parameters are contravariant, so Callable[[str, Animal], None]
    # is NOT a subtype of Callable[[str, Dog], None]
    schedule_feeding(feed_animal)  # This actually works due to contravariance


# Generic variance violation

T_co = TypeVar('T_co', covariant=True)
T_contra = TypeVar('T_contra', contravariant=True)

class Producer(Generic[T_co]):
    """Covariant producer."""
    
    def produce(self) -> T_co:
        raise NotImplementedError


class Consumer(Generic[T_contra]):
    """Contravariant consumer."""
    
    def consume(self, item: T_contra) -> None:
        raise NotImplementedError


class AnimalProducer(Producer[Animal]):
    """Produces animals."""
    def produce(self) -> Animal:
        return Animal()


class DogProducer(Producer[Dog]):
    """Produces dogs."""
    def produce(self) -> Dog:
        return Dog()


def use_producer(producer: Producer[Animal]) -> None:
    """
    LLM might think: "DogProducer can be used as Producer[Animal]"
    But mypy catches: Variance mismatch
    """
    animal = producer.produce()
    print(animal.speak())


def wrong_generic_covariance() -> None:
    """
    LLM might think: "Covariance allows this"
    But mypy catches: Producer[Dog] is not Producer[Animal]
    """
    dog_producer = DogProducer()
    # ERROR: Producer is covariant, so Producer[Dog] should be assignable to Producer[Animal]
    use_producer(dog_producer)  # This actually works


class AnimalConsumer(Consumer[Animal]):
    """Consumes animals."""
    def consume(self, animal: Animal) -> None:
        print(animal.speak())


class DogConsumer(Consumer[Dog]):
    """Consumes dogs."""
    def consume(self, dog: Dog) -> None:
        dog.fetch()


def use_consumer(consumer: Consumer[Dog], dog: Dog) -> None:
    """
    LLM might think: "AnimalConsumer can consume dogs"
    But mypy catches: Contravariance violation
    """
    consumer.consume(dog)


def wrong_generic_contravariance() -> None:
    """
    LLM might think: "Contravariance allows this"
    But mypy catches: Consumer[Animal] is not Consumer[Dog]
    """
    animal_consumer = AnimalConsumer()
    dog = Dog()
    # ERROR: Consumer is contravariant, so Consumer[Animal] should be assignable to Consumer[Dog]
    use_consumer(animal_consumer, dog)  # This actually works


# Iterator covariance violation

def iterate_animals(iterator: Iterator[Animal]) -> None:
    """
    LLM might think: "Iterator[Dog] can be used as Iterator[Animal]"
    But mypy catches: Iterator covariance
    """
    for animal in iterator:
        print(animal.speak())


def dog_iterator() -> Iterator[Dog]:
    """Create dog iterator."""
    yield Dog()
    yield Dog()


def wrong_iterator_covariance() -> None:
    """
    LLM might think: "Iterator covariance allows this"
    But mypy catches: Iterator[Dog] is not Iterator[Animal]
    """
    # ERROR: Iterator is covariant, so Iterator[Dog] should be assignable
    iterate_animals(dog_iterator())  # This actually works


# Protocol variance violation

class Drawable(Protocol[T_co]):
    """Covariant drawable protocol."""
    
    def draw(self) -> T_co: ...


class ShapeDrawer:
    """Draws shapes."""
    
    def draw(self) -> Animal:
        return Animal()


class DogDrawer:
    """Draws dogs."""
    
    def draw(self) -> Dog:
        return Dog()


def render_drawable(drawer: Drawable[Animal]) -> None:
    """
    LLM might think: "DogDrawer can be used as Drawable[Animal]"
    But mypy catches: Protocol variance
    """
    shape = drawer.draw()
    print(shape.speak())


def wrong_protocol_covariance() -> None:
    """
    LLM might think: "Protocol covariance allows this"
    But mypy catches: DogDrawer is not Drawable[Animal]
    """
    dog_drawer = DogDrawer()
    # ERROR: Protocol is covariant, so DogDrawer should be assignable
    render_drawable(dog_drawer)  # This actually works


# Mixed variance violation

class Processor(Generic[T_contra, T_co]):
    """Processor with mixed variance."""
    
    def process(self, input_data: T_contra) -> T_co:
        raise NotImplementedError


class AnimalProcessor(Processor[Animal, str]):
    """Processes animals to strings."""
    def process(self, animal: Animal) -> str:
        return animal.speak()


class DogProcessor(Processor[Dog, str]):
    """Processes dogs to strings."""
    def process(self, dog: Dog) -> str:
        return f"Dog says: {dog.speak()}"


def use_processor(processor: Processor[Dog, str], dog: Dog) -> str:
    """
    LLM might think: "AnimalProcessor can process dogs"
    But mypy catches: Mixed variance issues
    """
    return processor.process(dog)


def wrong_mixed_variance() -> None:
    """
    LLM might think: "Contravariance in input allows this"
    But mypy catches: Processor[Animal, str] is not Processor[Dog, str]
    """
    animal_processor = AnimalProcessor()
    dog = Dog()
    # ERROR: Due to contravariance in T_contra, Processor[Animal, str] should be assignable
    result = use_processor(animal_processor, dog)  # This actually works
