from typing import Callable, Any
import time

def wait_before_execute(wait_time_seconds: float = 1) -> Callable:
    def decorator(func: Callable):
        def wrapper(*args, **kwargs):
            time.sleep(wait_time_seconds)
            return func(*args, **kwargs)
        return wrapper
    return decorator

def retry_if_exception_raised(exceptions: Any) -> Callable:
    def decorator(func: callable):
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except exceptions:
                return func(*args, **kwargs)
        return wrapper
    return decorator

if __name__ == '__main__':
    pass