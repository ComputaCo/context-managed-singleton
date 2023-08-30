# Context Managed Data Structures

This is a Python utility module that provides a base class for creating a context that can be used in a context manager. The purpose of the context manager is to allow for easy management of the state of the context in a multithreaded environment where the context needs to be accessed and modified by multiple threads simultaneously.

## Usage
### Basic Usage
```python
from context_managed_data_structures import Context

# Create an instance of Context
ctx = Context()

# Use the instance in a with block
with ctx:
    # Do something with ctx
    ...

# The instance is automatically removed from the stack when the with block is exited
```

### Advanced Usage
The `Context` class can be subclassed to create a custom context with additional functionality. The class can also be wrapped around an existing class using the wrap static method.

```python
from context_managed_data_structures import Context

# Subclass the Context class
class MyClass(Context):
    ...

# (alternatively, wrap with Context.wrap decorator)
# @Context.wrap
# class MyClass:


def foo():
    # don't bother forwarding the instance to foo()
    # just get the current instance from the .current() class method
    my_instance = MyClass.current()
    ...

with MyClass():
    # lots of code and deeply buried calls to foo()
    ...

```

### Nested Contexts
The Context class can be used in nested contexts.

```python
from context_managed_data_structures import Context

# Create an instance of Context
ctx = Context()

# Use the instance in a with block
with ctx:
    # Do something with the context
    ...

    # Create a nested context
    with ctx:
        # Do something with the nested context
        ...

# The instances are automatically removed from the stack when the with blocks are exited
```

### Recursive Attribute Access
The Context class supports recursive attribute access. When an attribute is not found on the current instance, the class will look for the attribute on the previous instance in the stack.

```python
from context_managed_data_structures import Context

# create and enter a context
with Context({"a": 1, "b": 2}):
    with Context({"a": 4}, getattr_recursive=True):
        print(Context.current().a)  # prints 4
        print(Context.current().b)  # prints 2
    print(Context.current().a)  # prints 1
    print(Context.current().b)  # prints 2

# The instances are automatically removed from the stack when the with blocks are exited
```

## Tests
The tests for the Context class can be found in the tests directory. To run the tests, run the following command:

```bash
python -m unittest discover tests
```

## License
This project is licensed under the MIT License. See the LICENSE file for more information.