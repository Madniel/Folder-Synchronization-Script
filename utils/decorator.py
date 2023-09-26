from typing import Callable, Any
from functools import wraps
import logging

logging.basicConfig(level=logging.ERROR, format='%(asctime)s - %(levelname)s - %(message)s')


def exception_handler(re_raise_exceptions: tuple = ()) -> Callable:
    """
    A decorator to catch exceptions, log them, and optionally re-raise critical exceptions.

    The decorator will catch all exceptions that occur in the decorated function. If the exception
    is of a type specified in the `re_raise_exceptions` tuple, it will be re-raised after being logged.
    Otherwise, the exception will just be logged and suppressed. Example:

    @exception_handler(re_raise_exceptions=(ValueError, KeyError))
    def some_function():
        # Some code...

    Args:
    - re_raise_exceptions (tuple, optional): A tuple of exception types that should be re-raised after logging.
      Defaults to an empty tuple, meaning no exceptions will be re-raised by default.

    Returns:
    - Callable: Wrapped function that handles exceptions.
    """

    def decorator(func: Callable[..., Any]) -> Callable[..., Any]:
        @wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            try:
                return func(*args, **kwargs)
            except Exception as e:
                logging.error(f"An error occurred in function '{func.__name__}': {str(e)}")

                if isinstance(e, re_raise_exceptions):
                    raise

        return wrapper

    return decorator
