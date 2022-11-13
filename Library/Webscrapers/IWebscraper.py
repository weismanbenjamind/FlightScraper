from Library.Validators.ChromedriverValidator import ChromedriverValidator
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from typing import Any, Callable
import time

class IWebscraper:
    _SECONDS_BETWEEN_COMMANDS = 5
    _TIMEOUT_TIME_SECONDS = 1

    def __init__(self, base_url: str, path_to_chromedriver: str) -> None:
        ChromedriverValidator().validate(path_to_chromedriver)
        self._path_to_chromedriver = path_to_chromedriver
        self._base_url = base_url
        self._webdriver = None
        self._where_from = ''
        self._where_to = ''
        self._start_date = ''
        self._end_date = ''
        
    def initialize_webdriver(self) -> None:
        self._webdriver = webdriver.Chrome(executable_path = self._path_to_chromedriver)

    def scrape(self, **kwargs) -> None:
        try:
            self._where_from = kwargs['where_from']
            self._where_to = kwargs['where_to']
            self._departure_date = kwargs['departure_date']
            self._return_date = kwargs['return_date']
        except KeyError as ex:
            raise Exception(f'Webscraper.scrape() needs kwarg {ex.args[0]}')

    def _find_element_by_xpath_with_wait(self, x_path: str, wait_time_seconds = _TIMEOUT_TIME_SECONDS) -> Any:
        return WebDriverWait(self._webdriver, wait_time_seconds).until(lambda x: x.find_element(By.XPATH, x_path))

    def _find_element_by_xpath_and_click(self, x_path: str, wait_time_seconds = _TIMEOUT_TIME_SECONDS) -> None:
        WebDriverWait(self._webdriver, wait_time_seconds).until(EC.element_to_be_clickable((By.XPATH, x_path))).click()

    def _wait_before_execute(func: Callable) -> Callable:
        def wrapper(*args, **kwargs) -> Any:
            time.sleep(IWebscraper._SECONDS_BETWEEN_COMMANDS)
            func(*args, **kwargs)
        return wrapper

    def _wait_before_execute_with_return(func: Callable) -> Any:
        def wrapper(*args, **kwargs) -> Any:
            time.sleep(IWebscraper._SECONDS_BETWEEN_COMMANDS)
            return func(*args, **kwargs)
        return wrapper

    def close(self) -> None:
        self._webdriver.close()

if __name__ == '__main__':
    pass