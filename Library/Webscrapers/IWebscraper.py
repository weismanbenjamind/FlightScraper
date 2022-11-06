import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from Library.Validators.ChromedriverValidator import ChromedriverValidator
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
        

    def scrape(elf, home: str, destination: str, start_date: datetime, end_date: datetime ) -> pd.DataFrame:
        raise NotImplementedError('IWebscraper.scrape() is a virtual method and needs to be overriden')

    def _find_element_with_wait(self, by: By, element: Any, wait_time_seconds = 10):
        return WebDriverWait(self._webdriver, wait_time_seconds).until(lambda x: x.find_element(by, element))

    def _reset(self):
        self._where_from = ''
        self._where_to = ''
        self._start_date = None
        self._end_date = None

    def close(self):
        self._reset()
        self._webdriver.close()

if __name__ == '__main__':
    pass