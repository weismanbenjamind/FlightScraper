from Library.Webscrapers.IWebscraper import IWebscraper
from Library.Webscrapers.Decorators import wait_before_execute
from Library.Webscrapers.GoogleFlightsWebscraper import XPaths
from Library.DataParsers.GoogleFlightsDataParser import GoogleFlightsDataParser
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.action_chains import ActionChains
import pandas as pd

class GoogleFlightsWebscraper(IWebscraper):

    def __init__(self, base_url: str, path_to_chromedriver: str) -> None:
        super().__init__(base_url, path_to_chromedriver)
        self._data_parser = GoogleFlightsDataParser()
        self._departure_date_is_set = False
        self._return_date_is_set = False

    def scrape(self, **kwargs) -> pd.DataFrame:
        super()._initialize(**kwargs)
        self._webdriver.get(self._base_url)
        self._input_where_from()
        self._input_where_to()
        self._input_departure_date()
        self._input_return_date()
        self._click_done()
        self._click_more_flights()
        flight_data = self._get_flight_data()
        self._reset()
        return flight_data

    def _input_to_text_box_with_update(self, x_path_pre_input: str, xpath_after_input: str, input_text: str) -> None:
        text_box = self._find_element_by_xpath_with_wait(x_path_pre_input)
        text_box.clear()
        text_box.send_keys(input_text[0])
        text_box = self._find_element_by_xpath_with_wait(xpath_after_input)
        text_box.send_keys(input_text[1:])
        text_box.send_keys(Keys.RETURN)

    def _input_where_from(self) -> None:
        self._input_to_text_box_with_update(
            XPaths.WHERE_FROM_INPUT_BOX_PRE_INPUT_XPATH, 
            XPaths.WHERE_FROM_INPUT_BOX_AFTER_INPUT_XPATH, self._where_from
        )

    def _input_where_to(self) -> None:
        self._input_to_text_box_with_update(
            XPaths.WHERE_TO_INPUT_BOX_PRE_INPUT_XPATH, 
            XPaths.WHERE_TO_INPUT_BOX_AFTER_INPUT_XPATH, self._where_to
        )

    @wait_before_execute(IWebscraper._SECONDS_BETWEEN_COMMANDS)
    def _input_departure_date(self) -> None:
        date_box = self._find_element_by_xpath_with_wait(XPaths.DEPARTURE_DATE_INPUT_BOX_PRE_INPUT_XPATH)
        date_box.click()
        date_box = self._find_element_by_xpath_with_wait(XPaths.DEPARTURE_DATE_INPUT_BOX_AFTER_INPUT_XPATH)
        self._select_all_in_input_box()
        date_box.send_keys(Keys.BACK_SPACE)
        date_box.send_keys(self._departure_date)
        self._departure_date_is_set = True

    def _input_return_date(self) -> None:
        if not self._input_departure_date:
            raise RuntimeError('Need to call _input_departure_date() before _input_return_date()')
        date_box = self._find_element_by_xpath_with_wait(XPaths.RETURN_DATE_INPUT_BOX_PRE_INPUT_XPATH)
        date_box.click()
        self._select_all_in_input_box()
        date_box.send_keys(Keys.BACK_SPACE)
        date_box.send_keys(self._return_date)
        self._return_date_is_set = True

    def _click_done(self) -> None:
        if not self._return_date_is_set:
            raise RuntimeError('Need to call _input_return_date() before _click_done()')
        self._find_element_by_xpath_and_click(XPaths.DONE_X_PATH)
        self._return_date_is_set = False

    @wait_before_execute(IWebscraper._SECONDS_BETWEEN_COMMANDS)
    def _click_search(self) -> None:
        self._find_element_by_xpath_and_click(XPaths.SEARCH_BUTTON_XPATH)

    @wait_before_execute(IWebscraper._SECONDS_BETWEEN_COMMANDS)
    def _click_more_flights(self) -> None:
        max_more_flights_list_elements = 100
        for i in range(1, max_more_flights_list_elements):
            try:
                self._find_element_by_xpath_and_click(XPaths.MORE_FLIGHTS_BUTTON_X_PATH_TEMPALTE.format(i))
                return
            except TimeoutException:
                pass
        raise RuntimeError('Could not find more flights button')

    @wait_before_execute(IWebscraper._SECONDS_BETWEEN_COMMANDS)
    def _get_flight_data(self) -> pd.DataFrame:
        best_flights_data_string = ''
        other_flight_data_string = ''
        try:
            best_flights_data_string = self._find_element_by_xpath_with_wait(XPaths.BEST_FLIGHTS_X_PATH).text
        except Exception as ex:
            print(f'Could not best flights for {self._where_from}, {self._where_to}, {self._departure_date}, {self._return_date}')
        try:
            other_flight_data_string = self._find_element_by_xpath_with_wait(XPaths.MORE_FLIGHTS_X_PATH).text
        except Exception as ex:
            print(f'Could not find more flights for {self._where_from}, {self._where_to}, {self._departure_date}, {self._return_date}')
        return self._data_parser.parse([best_flights_data_string, other_flight_data_string], self._departure_date, self._return_date)

    def _reset(self) -> None:
        self._departure_date_is_set = False
        self._return_date_is_set = False
        super()._reset()

    def _close(self) -> None:
        self._reset()
        super._close()

if __name__ == '__main__':
    pass