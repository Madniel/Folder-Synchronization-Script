from typing import Callable, Any


def exception_handler(func: Callable[..., Any]) -> Callable[..., Any]:
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            print(f"An error occurred in function '{func.__name__}': {e}")
    return wrapper