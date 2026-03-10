"""
Obvious name errors and undefined variables.
"""
def undefined_variable():
    """Using variable that doesn't exist."""
    return undefined_name

def typo_in_variable():
    """Typo in variable name."""
    my_variable = 42
    return my_varible  # Typo: my_varible instead of my_variable

def undefined_function_call():
    """Calling function that doesn't exist."""
    return nonexistent_function()

def wrong_case():
    """Wrong case sensitivity."""
    MyVariable = "hello"
    return myvariable  # Wrong case

def import_error():
    """Importing non-existent module."""
    import nonexistent_module
    return nonexistent_module.some_function()

def attribute_error():
    """Accessing non-existent attribute."""
    obj = "string"
    return obj.nonexistent_attribute

def module_attribute_error():
    """Accessing non-existent module attribute."""
    import math
    return math.nonexistent_function

def builtin_name_error():
    """Misspelling builtin function."""
    return len("hello")  # This is fine
    # But if we had: return lenght("hello")  # Typo

def lenght(s):  # Wrong spelling
    """Wrong spelling of length."""
    return len(s)

def use_wrong_spelling():
    """Using wrong spelling."""
    return lenght("hello")

class ClassWithError:
    """Class with attribute error."""
    
    def __init__(self):
        self.value = 42
    
    def get_value(self):
        return self.val  # Typo: val instead of value

def call_undefined_method():
    """Calling undefined method."""
    obj = ClassWithError()
    return obj.undefined_method()

def recursive_undefined():
    """Recursive call to undefined function."""
    return recursive_undefined() + 1
