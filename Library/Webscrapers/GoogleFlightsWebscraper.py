from Library.Webscrapers.IWebscraper import IWebscraper
from Library.DataParsers.GoogleFlightsDataParser import GoogleFlightsDataParser
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.action_chains import ActionChains
import pandas as pd

class GoogleFlightsWebscraper(IWebscraper):
    
    _WHERE_FROM_INPUT_BOX_PRE_INPUT_XPATH = '/html/body/c-wiz[2]/div/div[2]/c-wiz/div[1]/c-wiz/div[2]/div[1]/div[1]/div[1]/div/div[2]/div[1]/div[1]/div/div/div[1]/div/div/input'
    _WHERE_FROM_INPUT_BOX_AFTER_INPUT_XPATH = '/html/body/c-wiz[2]/div/div[2]/c-wiz/div[1]/c-wiz/div[2]/div[1]/div[1]/div[1]/div/div[2]/div[1]/div[6]/div[2]/div[2]/div[1]/div/input'

    _WHERE_TO_INPUT_BOX_PRE_INPUT_XPATH = '/html/body/c-wiz[2]/div/div[2]/c-wiz/div[1]/c-wiz/div[2]/div[1]/div[1]/div[1]/div/div[2]/div[1]/div[4]/div/div/div[1]/div/div/input'
    _WHERE_TO_INPUT_BOX_AFTER_INPUT_XPATH = '/html/body/c-wiz[2]/div/div[2]/c-wiz/div[1]/c-wiz/div[2]/div[1]/div[1]/div[1]/div/div[2]/div[1]/div[6]/div[2]/div[2]/div[1]/div/input'

    _DEPARTURE_DATE_INPUT_BOX_PRE_INPUT_XPATH = '/html/body/c-wiz[2]/div/div[2]/c-wiz/div[1]/c-wiz/div[2]/div[1]/div[1]/div[1]/div/div[2]/div[2]/div/div/div[1]/div/div/div[1]/div/div[1]/div/input'
    _DEPARTURE_DATE_INPUT_BOX_AFTER_INPUT_XPATH = '/html/body/c-wiz[2]/div/div[2]/c-wiz/div[1]/c-wiz/div[2]/div[1]/div[1]/div[1]/div/div[2]/div[2]/div/div/div[2]/div/div[2]/div[1]/div[1]/div[1]/div/input'
    _RETURN_DATE_INPUT_BOX_PRE_INPUT_XPATH = '/html/body/c-wiz[2]/div/div[2]/c-wiz/div[1]/c-wiz/div[2]/div[1]/div[1]/div[1]/div/div[2]/div[2]/div/div/div[2]/div/div[2]/div[1]/div[1]/div[2]/div/input'
    _RETURN_DATE_INPUT_BOX_AFTER_INPUT_XPATH = '/html/body/c-wiz[2]/div/div[2]/c-wiz/div[1]/c-wiz/div[2]/div[1]/div[1]/div[1]/div/div[2]/div[2]/div/div/div[2]/div/div[2]/div[1]/div[1]/div[2]/div/input'

    _SEARCH_BUTTON_XPATH = '/html/body/c-wiz[2]/div/div[2]/c-wiz/div[1]/c-wiz/div[2]/div[1]/div[1]/div[2]/div/button'
    _MORE_FLIGHTS_BUTTON_X_PATH_TEMPALTE = '/html/body/c-wiz[2]/div/div[2]/c-wiz/div[1]/c-wiz/div[2]/div[2]/div[5]/ul/li[{}]/div/span[1]/div/button'

    _BEST_FLIGHTS_X_PATH = '/html/body/c-wiz[2]/div/div[2]/c-wiz/div[1]/c-wiz/div[2]/div[2]/div[3]/ul'
    _MORE_FLIGHTS_X_PATH = '/html/body/c-wiz[2]/div/div[2]/c-wiz/div[1]/c-wiz/div[2]/div[2]/div[5]/ul'

    _DONE_X_PATH = '/html/body/c-wiz[2]/div/div[2]/c-wiz/div[1]/c-wiz/div[2]/div[1]/div[1]/div[1]/div/div[2]/div[2]/div/div/div[2]/div/div[3]/div[3]/div/button'
    

    def __init__(self, base_url: str, path_to_chromedriver: str) -> None:
        super().__init__(base_url, path_to_chromedriver)
        self._data_parser = GoogleFlightsDataParser()
        self._departure_date_is_set = False
        self._return_date_is_set = False

    def scrape(self, **kwargs) -> pd.DataFrame:
        super().scrape(**kwargs)
        self._webdriver.get(self._base_url)
        self._input_where_from()
        self._input_where_to()
        self._input_departure_date()
        self._input_return_date()
        self._click_done()
        self._click_more_flights()
        return self._get_flight_data()

    def _input_to_text_box_with_update(self, x_path_pre_input: str, xpath_after_input: str, input_text: str) -> None:
        text_box = self._find_element_by_xpath_with_wait(x_path_pre_input)
        text_box.clear()
        text_box.send_keys(input_text[0]) # Send first key - will cause a change in x-path
        text_box = self._find_element_by_xpath_with_wait(xpath_after_input) # Get the new text box
        text_box.send_keys(input_text[1:]) # Send the rest of the keys
        text_box.send_keys(Keys.RETURN) # Hit return to get out of text box

    def _input_where_from(self) -> None:
        self._input_to_text_box_with_update(self._WHERE_FROM_INPUT_BOX_PRE_INPUT_XPATH, self._WHERE_FROM_INPUT_BOX_AFTER_INPUT_XPATH, self._where_from)

    def _input_where_to(self) -> None:
        self._input_to_text_box_with_update(self._WHERE_TO_INPUT_BOX_PRE_INPUT_XPATH, self._WHERE_TO_INPUT_BOX_AFTER_INPUT_XPATH, self._where_to)

    ###TODO - FIX THIS BLOCK - NEED TO PROPERLY ACQUIRE DATES ###

    @IWebscraper._wait_before_execute
    def _input_departure_date(self) -> None:
        date_box = self._find_element_by_xpath_with_wait(self._DEPARTURE_DATE_INPUT_BOX_PRE_INPUT_XPATH)
        date_box.click()
        date_box = self._find_element_by_xpath_with_wait(self._DEPARTURE_DATE_INPUT_BOX_AFTER_INPUT_XPATH)
        ActionChains(self._webdriver).key_down(Keys.COMMAND).send_keys('a').key_up(Keys.COMMAND).perform()
        date_box.send_keys(Keys.BACK_SPACE)
        date_box.send_keys(self._departure_date)
        self._departure_date_is_set = True

    def _input_return_date(self):
        if not self._input_departure_date:
            raise RuntimeError('Need to call _input_departure_date() before _input_return_date()')
        date_box = self._find_element_by_xpath_with_wait(self._RETURN_DATE_INPUT_BOX_PRE_INPUT_XPATH)
        date_box.click()
        ActionChains(self._webdriver).key_down(Keys.COMMAND).send_keys('a').key_up(Keys.COMMAND).perform()
        date_box.send_keys(Keys.BACK_SPACE)
        date_box.send_keys(self._return_date)
        self._departure_date_is_set = False
        self._return_date_is_set = True

    def _click_done(self):
        if not self._return_date_is_set:
            raise RuntimeError('Need to call _input_return_date() before _click_done()')
        self._find_element_by_xpath_and_click(self._DONE_X_PATH)
        self._return_date_is_set = False

    ### FINISH SECTION TO FIX ###

    @IWebscraper._wait_before_execute
    def _click_search(self):
        self._find_element_by_xpath_and_click(self._SEARCH_BUTTON_XPATH)

    @IWebscraper._wait_before_execute
    def _click_more_flights(self):
        max_more_flights_list_elements = 100
        for i in range(1, max_more_flights_list_elements):
            try:
                self._find_element_by_xpath_and_click(self._MORE_FLIGHTS_BUTTON_X_PATH_TEMPALTE.format(i))
                return
            except TimeoutException:
                pass
        raise RuntimeError('Could not find more flights button')

    @IWebscraper._wait_before_execute_with_return
    def _get_flight_data(self) -> pd.DataFrame:
        best_flights_data_string = self._find_element_by_xpath_with_wait(self._BEST_FLIGHTS_X_PATH).text
        other_flight_data_string = self._find_element_by_xpath_with_wait(self._MORE_FLIGHTS_X_PATH).text
        return self._data_parser.parse([best_flights_data_string, other_flight_data_string], self._departure_date, self._return_date)

if __name__ == '__main__':
    pass