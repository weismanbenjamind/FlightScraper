from Library.Webscrapers.IWebscraper import IWebscraper
from typing import Callable
import time

def wait_before_execute(wait_time_seconds: str) -> Callable:
    def decorator(func: Callable):
        def wrapper(*args, **kwargs):
            time.sleep(wait_time_seconds)
            return func(*args, **kwargs)
        return wrapper
    return decorator

if __name__ == '__main__':
    pass