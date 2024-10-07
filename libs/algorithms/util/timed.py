import functools
import time
from typing import Callable, Any


# a decorator to measure the execution time
def timed():
    def wrapper(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapped(*args, **kwargs) -> Any:
            # print(f'{func.__name__} called with : {args}, {kwargs}.')
            # print(f'{func.__name__} called.')
            start = time.time()
            try:
                return func(*args, **kwargs)
            finally:
                end = time.time()
                total = end - start
                print(f'{func.__name__} has taken {total:.10f} seconds.')

        return wrapped

    return wrapper


@timed()
def timed_func(func, *args, **kwargs):
    return func(*args, **kwargs)
