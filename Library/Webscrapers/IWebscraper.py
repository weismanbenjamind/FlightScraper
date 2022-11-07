from Library.Validators.ChromedriverValidator import ChromedriverValidator
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from datetime import datetime
from typing import Any

class IWebscraper:

    def __init__(self, base_url: str, path_to_chromedriver: str) -> None:
        ChromedriverValidator().validate(path_to_chromedriver)
        self._path_to_chromedriver = path_to_chromedriver
        self._base_url = base_url
        self._webdriver = webdriver.Chrome(executable_path = path_to_chromedriver)
        self._where_from = ''
        self._where_to = ''
        self._start_date = None
        self._end_date = None
        

    def scrape(self, **kwargs) -> None:
        try:
            self._where_from = kwargs['where_from']
            self._where_to = kwargs['where_to']
            self._start_date = kwargs['departure_date']
            self._end_date = kwargs['return_date']
        except KeyError as ex:
            raise Exception(f'Webscraper.scrape() needs kwarg {ex.args[0]}')

    def _find_element_with_wait(self, by: By, element: Any, wait_time_seconds = 10) -> Any:
        return WebDriverWait(self._webdriver, wait_time_seconds).until(lambda x: x.find_element(by, element))

    def close(self) -> None:
        self._reset()
        self._webdriver.close()

if __name__ == '__main__':
    pass