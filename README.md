Context Managed Singleton
This is a Python utility module that provides a base class for creating a singleton that can be used in a context manager. The purpose of the context manager is to allow for easy management of the state of the singleton in a multithreaded environment where the singleton needs to be accessed and modified by multiple threads simultaneously.

## Usage
### Basic Usage
```python
from context_managed_singleton import ContextManagedSingleton

# Create an instance of ContextManagedSingleton
ctx = ContextManagedSingleton()

# Use the instance in a with block
with ctx:
    # Do something with the singleton
    ...

# The instance is automatically removed from the stack when the with block is exited
```

### Advanced Usage
The ContextManagedSingleton class can be subclassed to create a custom singleton with additional functionality. The class can also be wrapped around an existing class using the wrap static method.

```python
from context_managed_singleton import ContextManagedSingleton

# Subclass the ContextManagedSingleton class
class MyClass(ContextManagedSingleton):
    ...

# (alternatively, wrap with ContextManagedSingleton.wrap decorator)
# @ContextManagedSingleton.wrap
# class MyClass:


def foo():
    # don't bother forwarding the instance to foo()
    # just get the current instance from the .current() class method
    my_instance = MyClass.current()
    ...

with MySingleton():
    # lots of code and deeply buried calls to foo()
    ...

```

### Nested Contexts
The ContextManagedSingleton class can be used in nested contexts.

```python
from context_managed_singleton import ContextManagedSingleton

# Create an instance of ContextManagedSingleton
ctx = ContextManagedSingleton()

# Use the instance in a with block
with ctx:
    # Do something with the singleton
    ...

    # Create a nested context
    with ctx:
        # Do something with the nested singleton
        ...

# The instances are automatically removed from the stack when the with blocks are exited
```

### Recursive Attribute Access
The ContextManagedSingleton class supports recursive attribute access. When an attribute is not found on the current instance, the class will look for the attribute on the previous instance in the stack.

```python
from context_managed_singleton import ContextManagedSingleton

# create and enter a context
with ContextManagedSingleton({"a": 1, "b": 2}):
    with ContextManagedSingleton({"a": 4}, getattr_recursive=True):
        print(ContextManagedSingleton.current().a)  # prints 4
        print(ContextManagedSingleton.current().b)  # prints 2
    print(ContextManagedSingleton.current().a)  # prints 1
    print(ContextManagedSingleton.current().b)  # prints 2

# The instances are automatically removed from the stack when the with blocks are exited
```

## Tests
The tests for the ContextManagedSingleton class can be found in the tests directory. To run the tests, run the following command:

```bash
python -m unittest discover tests
```

## License
This project is licensed under the MIT License. See the LICENSE file for more information.