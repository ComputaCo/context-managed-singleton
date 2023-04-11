from __future__ import annotations
from contextlib import contextmanager
from typing import Any, Optional, Type, TypeVar

T = TypeVar("T", bound="Type")


class ContextManagedSingleton:
    """A singleton class that maintains a stack of instances in a context.

    This class can be subclassed or wrapped around another class using the
    `wrap` static method. Optionally, it allows for recursive attribute search
    across the stack and can bake public attributes of a given object into
    the instance's __dict__.
    """

    __current: dict = {}

    def __init__(
        self, baked_obj: Optional[Any] = None, /, *, getattr_recursive: bool = False
    ) -> None:
        """Initialize a new instance of the class.

        Args:
            baked_obj (Optional[Any]): An object, dict, or anything else that supports `dir`.
                If supplied, all the public attributes of the argument will be
                baked into the instance's __dict__. Default is None.
            getattr_recursive (bool): If set to True, enables recursive attribute
                search up the stack when an attribute is not found. Default is False.
        """
        self.__getattr_recursive = getattr_recursive

        if isinstance(baked_obj, dict):
            self.__dict__.update(baked_obj)
        elif isinstance(baked_obj, object):
            self.__dict__.update(
                {
                    attr: getattr(baked_obj, attr)
                    for attr in dir(baked_obj)
                    if not attr.startswith("_")
                }
            )

    @classmethod
    def current(cls) -> "ContextManagedSingleton":
        """Return the most recent instance that entered the context.

        Returns:
            ContextManagedSingleton: The current instance at the top of the stack.

        Raises:
            RuntimeError: If no instance has entered the context.
        """
        if cls not in cls.__current or not cls.__current[cls]:
            raise RuntimeError("No instance of the class has entered the context.")
        return cls.__current[cls][-1]

    def __enter__(self) -> "ContextManagedSingleton":
        """Push the instance to the context stack and return itself.

        Returns:
            ContextManagedSingleton: The current instance.
        """
        if self.__class__ not in self.__current:
            self.__current[self.__class__] = []
        self.__current[self.__class__].append(self)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Pop the current instance from the context stack."""
        assert self.__current[self.__class__][-1] is self, "Unbalanced context stack."

        self.__current[self.__class__].pop()

    def __getattr__(self, name: str) -> Any:
        """Retrieve an attribute from the instance, optionally searching the stack recursively.

        Args:
            name (str): The name of the attribute.

        Returns:
            Any: The value of the attribute.

        Raises:
            AttributeError: If the attribute is not found.
        """
        try:
            return super().__getattr__(self, name)
        except:
            if (
                self.__class__ in self.__current
                and len(self.__current[self.__class__]) > 1
                and self.__getattr_recursive
            ):
                return getattr(self.__current[self.__class__][-2], name)
            raise AttributeError(
                f"'{self.__class__.__name__}' object has no attribute '{name}'"
            )

    @staticmethod
    def wrap(target_class: T) -> T:
        """Subclass the target class with ContextManagedSingleton
        Args:
            target_class (T): The class to be wrapped.

        Returns:
            T: A new class that subclasses both the target class and ContextManagedSingleton.
        """

        class Wrapped(target_class, ContextManagedSingleton):
            pass

        Wrapped.__name__ = target_class.__name__
        Wrapped.__module__ = target_class.__module__
        return Wrapped
