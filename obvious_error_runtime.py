"""
Obvious type errors and runtime errors.
"""
def type_mismatch():
    """Obvious type mismatch."""
    number = 42
    text = "hello"
    return number + text  # Can't add int and str

def index_error():
    """Index out of range."""
    my_list = [1, 2, 3]
    return my_list[10]  # Index 10 doesn't exist

def key_error():
    """Key doesn't exist in dict."""
    my_dict = {"a": 1, "b": 2}
    return my_dict["c"]  # Key "c" doesn't exist

def attribute_error():
    """Attribute doesn't exist."""
    my_string = "hello"
    return my_string.length  # Strings don't have 'length' attribute

def zero_division():
    """Division by zero."""
    return 10 / 0

def wrong_function_call():
    """Wrong number of arguments."""
    def takes_two_args(a, b):
        return a + b
    
    return takes_two_args(1)  # Missing second argument

def wrong_type_argument():
    """Wrong type of argument."""
    def takes_string(s):
        return len(s)
    
    return takes_string(42)  # Passing int instead of str

def list_index_with_string():
    """Using string as list index."""
    my_list = [1, 2, 3]
    return my_list["first"]  # Can't index list with string

def dict_key_with_list():
    """Using list as dict key."""
    my_dict = {}
    my_dict[[1, 2, 3]] = "value"  # Lists are not hashable

def call_int_as_function():
    """Trying to call int as function."""
    number = 42
    return number()  # Can't call int

def string_concat_error():
    """Wrong string concatenation."""
    name = "Alice"
    age = 30
    return name + age  # Can't concatenate str and int

def list_append_error():
    """Wrong type to list append."""
    my_list = []
    my_list.append(1, 2)  # append takes only one argument

def file_operation_error():
    """File operation without proper handling."""
    file = open("nonexistent_file.txt")  # File doesn't exist
    return file.read()

def import_and_use_error():
    """Import and use wrong way."""
    import os
    return os.nonexistent_path  # nonexistent_path doesn't exist

def range_error():
    """Range with wrong arguments."""
    return list(range("a", "z"))  # range expects ints

def max_error():
    """Max with incompatible types."""
    return max([1, 2, "three"])  # Can't compare int and str

def sort_error():
    """Sort incompatible types."""
    my_list = [1, 2, "three"]
    my_list.sort()  # Can't sort mixed types
    return my_list

def set_operation_error():
    """Set operation with unhashable type."""
    my_set = {1, 2, 3}
    my_set.add([4, 5])  # Can't add list to set

def tuple_unpack_error():
    """Wrong unpacking."""
    my_tuple = (1, 2, 3)
    a, b = my_tuple  # Too many values to unpack

def format_error():
    """Wrong string formatting."""
    return "Hello {}".format()  # Missing argument

def json_error():
    """JSON with invalid data."""
    import json
    return json.dumps(set([1, 2, 3]))  # Sets are not JSON serializable