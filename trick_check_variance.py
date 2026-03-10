"""
Variance in type systems that LLMs often get wrong.
These look like type mismatches but are actually valid.
"""
from typing import Callable, List, Sequence, Generic, TypeVar, Protocol

# Covariance example

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
    LLM might flag: "List[Dog] not compatible with Sequence[Animal]"
    But Sequence is covariant, so this is CORRECT.
    """
    for animal in animals:
        print(animal.speak())


def test_covariance() -> None:
    """Test covariance."""
    dogs: List[Dog] = [Dog(), Dog()]
    # Covariance allows this
    process_animals(dogs)


# Contravariance example

def handle_dog(dog: Dog) -> None:
    """Handle a dog."""
    dog.fetch()


def handle_animal(animal: Animal) -> None:
    """Handle any animal."""
    print(animal.speak())


def register_handler(handler: Callable[[Dog], None]) -> None:
    """
    LLM might flag: "Callable[[Animal], None] not compatible with Callable[[Dog], None]"
    But contravariance makes this CORRECT.
    """
    dog = Dog()
    handler(dog)


def test_contravariance() -> None:
    """Test contravariance."""
    # Contravariance allows passing handle_animal where Dog handler expected
    register_handler(handle_animal)


# Return type covariance

def create_animal() -> Animal:
    """Create any animal."""
    return Animal()


def create_dog() -> Dog:
    """Create a dog."""
    return Dog()


def use_creator(creator: Callable[[], Animal]) -> None:
    """
    LLM might flag: "Callable[[], Dog] not compatible with Callable[[], Animal]"
    But return type covariance makes this CORRECT.
    """
    animal = creator()
    print(animal.speak())


def test_return_covariance() -> None:
    """Test return type covariance."""
    # Covariance allows this
    use_creator(create_dog)


# Parameter contravariance

def feed_dog(food: str, dog: Dog) -> None:
    """Feed a dog."""
    print(f"Feeding {food} to dog")


def feed_animal(food: str, animal: Animal) -> None:
    """Feed any animal."""
    print(f"Feeding {food} to animal")


def schedule_feeding(feeder: Callable[[str, Dog], None]) -> None:
    """
    LLM might flag: "Callable[[str, Animal], None] not compatible"
    But parameter contravariance makes this CORRECT.
    """
    feeder("bone", Dog())


def test_parameter_contravariance() -> None:
    """Test parameter contravariance."""
    # Contravariance allows this
    schedule_feeding(feed_animal)


# Generic variance

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
    LLM might flag: "DogProducer not compatible with Producer[Animal]"
    But covariance makes this CORRECT.
    """
    animal = producer.produce()
    print(animal.speak())


def test_generic_covariance() -> None:
    """Test generic covariance."""
    dog_producer = DogProducer()
    # Covariance allows this
    use_producer(dog_producer)


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
    LLM might flag: "AnimalConsumer not compatible with Consumer[Dog]"
    But contravariance makes this CORRECT.
    """
    consumer.consume(dog)


def test_generic_contravariance() -> None:
    """Test generic contravariance."""
    animal_consumer = AnimalConsumer()
    dog = Dog()
    # Contravariance allows this
    use_consumer(animal_consumer, dog)


# Protocol variance

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
    LLM might flag: "DogDrawer not compatible with Drawable[Animal]"
    But protocol covariance makes this CORRECT.
    """
    shape = drawer.draw()
    print(shape.speak())


def test_protocol_covariance() -> None:
    """Test protocol covariance."""
    dog_drawer = DogDrawer()
    # Covariance allows this
    render_drawable(dog_drawer)


# Iterator covariance

def iterate_animals(iterator: Iterator[Animal]) -> None:
    """
    LLM might flag: "Iterator[Dog] not compatible with Iterator[Animal]"
    But Iterator is covariant.
    """
    for animal in iterator:
        print(animal.speak())


def dog_iterator() -> Iterator[Dog]:
    """Create dog iterator."""
    yield Dog()
    yield Dog()


def test_iterator_covariance() -> None:
    """Test iterator covariance."""
    # Iterator covariance allows this
    iterate_animals(dog_iterator())


# Mixed variance scenarios

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
    LLM might flag: "AnimalProcessor not compatible"
    But contravariance in input makes this CORRECT.
    """
    return processor.process(dog)


def test_mixed_variance() -> None:
    """Test mixed variance."""
    animal_processor = AnimalProcessor()
    dog = Dog()
    # Contravariance allows this
    result = use_processor(animal_processor, dog)
    assert "sound" in result
