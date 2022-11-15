from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from typing import Any

class IWebscraper:
    _TIMEOUT_TIME_SECONDS = 10

    def __init__(self, base_url: str, path_to_chromedriver: str) -> None:
        self._path_to_chromedriver = path_to_chromedriver
        self._base_url = base_url
        self._webdriver = None
        self._where_from = ''
        self._where_to = ''
        self._start_date = ''
        self._end_date = ''
        
    def initialize_webdriver(self) -> None:
        self._webdriver = webdriver.Chrome(executable_path = self._path_to_chromedriver)

    def _initialize(self, **kwargs) -> None:
        try:
            self._where_from = kwargs['where_from']
            self._where_to = kwargs['where_to']
            self._departure_date = kwargs['departure_date']
            self._return_date = kwargs['return_date']
        except KeyError as ex:
            raise Exception(f'Webscraper.scrape() needs kwarg {ex.args[0]}')

    def scrape(self, **kwargs) -> None:
        raise NotImplementedError('IWebscraper.scrape() is a virtual method and needs to be overridden')

    def _find_element_by_xpath_with_wait(self, x_path: str, timeout_time_seconds: float = _TIMEOUT_TIME_SECONDS) -> Any:
        return WebDriverWait(self._webdriver, timeout_time_seconds).until(EC.presence_of_element_located((By.XPATH, x_path)))

    def _find_element_by_xpath_and_click(self, x_path: str, timeout_time_seconds: float = _TIMEOUT_TIME_SECONDS) -> None:
        WebDriverWait(self._webdriver, timeout_time_seconds).until(EC.element_to_be_clickable((By.XPATH, x_path))).click()

    def _select_all_in_input_box(self) -> None:
        ActionChains(self._webdriver).key_down(Keys.COMMAND).send_keys('a').key_up(Keys.COMMAND).perform()

    def _reset(self) -> None:
        self._where_from = ''
        self._where_to = ''
        self._start_date = ''
        self._end_date = ''

    def close(self) -> None:
        self._reset()
        self._webdriver.close()

if __name__ == '__main__':
    pass