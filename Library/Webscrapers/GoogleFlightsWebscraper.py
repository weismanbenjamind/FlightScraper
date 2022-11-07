from Library.Webscrapers.IWebscraper import IWebscraper
from typing import Any, Dict
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

class GoogleFlightsWebscraper(IWebscraper):
    
    _WHERE_FROM_INPUT_BOX_PRE_INPUT_XPATH = '/html/body/c-wiz[2]/div/div[2]/c-wiz/div[1]/c-wiz/div[2]/div[1]/div[1]/div[1]/div/div[2]/div[1]/div[1]/div/div/div[1]/div/div/input'
    _WHERE_FROM_INPUT_BOX_AFTER_INPUT_XPATH = '/html/body/c-wiz[2]/div/div[2]/c-wiz/div[1]/c-wiz/div[2]/div[1]/div[1]/div[1]/div/div[2]/div[1]/div[6]/div[2]/div[2]/div[1]/div/input'

    _WHERE_TO_INPUT_BOX_PRE_INPUT_XPATH = '/html/body/c-wiz[2]/div/div[2]/c-wiz/div[1]/c-wiz/div[2]/div[1]/div[1]/div[1]/div/div[2]/div[1]/div[4]/div/div/div[1]/div/div/input'
    _WHERE_TO_INPUT_BOX_AFTER_INPUT_XPATH = '/html/body/c-wiz[2]/div/div[2]/c-wiz/div[1]/c-wiz/div[2]/div[1]/div[1]/div[1]/div/div[2]/div[1]/div[6]/div[2]/div[2]/div[1]/div/input'

    def __init__(self, base_url: str, path_to_chromedriver: str) -> None:
        super().__init__(base_url, path_to_chromedriver)

    def scrape(self, **kwargs) -> None:
        super().scrape(**kwargs)
        self._webdriver.get(self._base_url)
        self._input_where_from()
        self._input_where_to()

    def _input_to_text_box_with_update(self, x_path_pre_input: str, xpath_after_input: str, input_text: str) -> None:
        text_box = self._find_element_with_wait(By.XPATH, x_path_pre_input)
        text_box.clear()
        text_box.send_keys(input_text[0]) # Send first key - will cause a change in x-path
        text_box = self._find_element_with_wait(By.XPATH, xpath_after_input) # Get the new text box
        text_box.send_keys(input_text[1:]) # Send the rest of the keys
        text_box.send_keys(Keys.RETURN) # Hit return to get out of text box

    def _input_where_from(self) -> None:
        self._input_to_text_box_with_update(self._WHERE_FROM_INPUT_BOX_PRE_INPUT_XPATH, self._WHERE_FROM_INPUT_BOX_AFTER_INPUT_XPATH, self._where_from)

    def _input_where_to(self) -> None:
        self._input_to_text_box_with_update(self._WHERE_TO_INPUT_BOX_PRE_INPUT_XPATH, self._WHERE_TO_INPUT_BOX_AFTER_INPUT_XPATH, self._where_to)

if __name__ == '__main__':
    pass