"""
Valid covariance and contravariance patterns that look suspicious to LLMs.
These are correct uses of variance in type systems.
"""
from typing import Callable, List, Sequence, Iterator, TypeVar, Generic

# Callable contravariance example

class Animal:
    """Base animal class."""
    def speak(self) -> str:
        return "Some sound"


class Dog(Animal):
    """Dog extends Animal."""
    def speak(self) -> str:
        return "Woof"
    
    def fetch(self) -> None:
        print("Fetching ball")


def process_dogs(handler: Callable[[Dog], None]) -> None:
    """Function that expects a handler for Dogs."""
    handler(Dog())


def handle_animal(animal: Animal) -> None:
    """Handler that accepts any Animal."""
    print(animal.speak())


def test_contravariance() -> None:
    """
    LLM might flag: "handle_animal expects Animal, but process_dogs wants Dog handler"
    But this is CORRECT - contravariance allows it.
    
    Why? If we pass handle_animal to process_dogs:
    - process_dogs will call handler(Dog())
    - handle_animal accepts Animal
    - Dog is Animal, so it's safe
    """
    # This is valid due to contravariance of callable arguments
    process_dogs(handle_animal)


# List covariance (read-only operations)

def iterate_animals(animals: Sequence[Animal]) -> None:
    """
    Sequence[Animal] is covariant - List[Dog] works!
    LLM might flag: "List[Dog] not compatible with Sequence[Animal]"
    But it's correct - Sequence is read-only.
    """
    for animal in animals:
        print(animal.speak())


def use_dog_list() -> None:
    """Use list of dogs where sequence of animals expected."""
    dogs: List[Dog] = [Dog(), Dog()]
    # This works because Sequence is covariant
    iterate_animals(dogs)


T = TypeVar('T', covariant=True)

class Producer(Generic[T]):
    """Covariant producer - only returns T."""
    
    def get(self) -> T:
        raise NotImplementedError


class AnimalProducer(Producer[Animal]):
    """Produces animals."""
    def get(self) -> Animal:
        return Animal()


class DogProducer(Producer[Dog]):
    """Produces dogs."""
    def get(self) -> Dog:
        return Dog()


def consume_animal_producer(producer: Producer[Animal]) -> None:
    """Consume any producer of animals."""
    animal = producer.get()
    print(animal.speak())


def use_covariant_producer() -> None:
    """
    LLM might flag: "DogProducer[Dog] not compatible with Producer[Animal]"
    But due to covariance, this is CORRECT!
    
    Why? Dog is subtype of Animal, so Producer[Dog] is subtype of Producer[Animal]
    """
    dog_producer = DogProducer()
    # Covariance allows this
    consume_animal_producer(dog_producer)


U = TypeVar('U', contravariant=True)

class Consumer(Generic[U]):
    """Contravariant consumer - only accepts U."""
    
    def accept(self, item: U) -> None:
        raise NotImplementedError


class AnimalConsumer(Consumer[Animal]):
    """Consumes animals."""
    def accept(self, animal: Animal) -> None:
        print(animal.speak())


class DogConsumer(Consumer[Dog]):
    """Consumes dogs."""
    def accept(self, dog: Dog) -> None:
        print(dog.speak())


def feed_consumer(consumer: Consumer[Dog], dog: Dog) -> None:
    """Feed a dog to a consumer that accepts dogs."""
    consumer.accept(dog)


def use_contravariant_consumer() -> None:
    """
    LLM might flag: "AnimalConsumer[Animal] not compatible with Consumer[Dog]"
    But due to contravariance, this is CORRECT!
    
    Why? If we pass AnimalConsumer to a function expecting Consumer[Dog]:
    - The function will call consumer.accept(dog)
    - AnimalConsumer.accept expects Animal
    - Dog is Animal, so it's safe
    """
    animal_consumer = AnimalConsumer()
    dog = Dog()
    # Contravariance allows passing AnimalConsumer where DogConsumer expected
    feed_consumer(animal_consumer, dog)


# Iterator covariance

def iterate_values(iterator: Iterator[Animal]) -> None:
    """Iterate over animals."""
    for animal in iterator:
        print(animal.speak())


def dog_iterator() -> Iterator[Dog]:
    """Create iterator of dogs."""
    yield Dog()
    yield Dog()


def use_iterator_covariance() -> None:
    """
    LLM might flag: "Iterator[Dog] not compatible with Iterator[Animal]"
    But Iterator is covariant, so this works.
    """
    # Iterator covariance allows this
    iterate_values(dog_iterator())


# Return type covariance

def get_animal() -> Animal:
    """Get any animal."""
    return Animal()


def get_dog() -> Dog:
    """Get a dog."""
    return Dog()


def fetch_and_speak(fetcher: Callable[[], Animal]) -> None:
    """Fetch and speak with any animal."""
    animal = fetcher()
    print(animal.speak())


def use_return_covariance() -> None:
    """
    LLM might flag: "Callable[[], Dog] not compatible with Callable[[], Animal]"
    But return types are covariant, so this is CORRECT.
    
    Why? If a function returns Dog where Animal expected:
    - We can treat Dog as Animal
    - This is safe due to the subtype relationship
    """
    # Return type covariance allows this
    fetch_and_speak(get_dog)


# Parameter contravariance in callbacks

def register_callback(callback: Callable[[Dog], None]) -> None:
    """Register a callback for dogs."""
    dog = Dog()
    callback(dog)


def handle_dog(dog: Dog) -> None:
    """Handle a dog specifically."""
    dog.fetch()


def handle_generic_animal(animal: Animal) -> None:
    """Handle any animal."""
    print(animal.speak())


def use_parameter_contravariance() -> None:
    """
    LLM might flag: "Callable[[Animal], None] not compatible with Callable[[Dog], None]"
    But parameter types are contravariant, so this is CORRECT!
    
    Why? If we pass handle_generic_animal where handle_dog expected:
    - The function will call callback(Dog())
    - handle_generic_animal accepts Animal
    - Dog is Animal, so it's safe
    """
    # Parameter contravariance allows this
    register_callback(handle_generic_animal)


# Mixed scenarios

class AnimalFactory:
    """Creates animals."""
    def create(self) -> Animal:
        return Animal()


class DogFactory(AnimalFactory):
    """Creates dogs."""
    def create(self) -> Dog:
        return Dog()


def use_factory(factory: AnimalFactory) -> None:
    """Use any animal factory."""
    animal = factory.create()
    print(animal.speak())


def use_dog_factory_as_animal() -> None:
    """
    LLM might flag: "DogFactory not compatible with AnimalFactory"
    But covariance of return types makes this CORRECT.
    """
    dog_factory = DogFactory()
    # Covariance in return types allows this
    use_factory(dog_factory)


V = TypeVar('V')

def apply(operation: Callable[[V], V], value: V) -> V:
    """Apply operation to value."""
    return operation(value)


def double(x: int) -> int:
    """Double a number."""
    return x * 2


def use_type_variable() -> None:
    """
    LLM might worry about type variable inference.
    But mypy correctly infers T=int here.
    """
    result = apply(double, 42)  # T inferred as int
    assert result == 84
