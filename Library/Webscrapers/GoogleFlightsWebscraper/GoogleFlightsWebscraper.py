from Library.Webscrapers.IWebscraper import IWebscraper
from Library.Webscrapers.Decorators import wait_before_execute, retry_if_exception_raised
from Library.Webscrapers.GoogleFlightsWebscraper import XPaths
from Library.DataParsers.GoogleFlightsDataParser import GoogleFlightsDataParser
from Library.Exceptions.HTMLNotFoundError import HTMLNotFoundError
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException, ElementNotInteractableException
import pandas as pd

class GoogleFlightsWebscraper(IWebscraper):

    def __init__(self, base_url: str, path_to_chromedriver: str) -> None:
        super().__init__(base_url, path_to_chromedriver)
        self._data_parser = GoogleFlightsDataParser()
        self._departure_date_is_set = False
        self._return_date_is_set = False
        self._found_more_flights_button = False

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

    @retry_if_exception_raised((TimeoutException, ElementNotInteractableException))
    def _input_where_from(self) -> None:
        self._input_to_text_box_with_update(
            XPaths.WHERE_FROM_INPUT_BOX_PRE_INPUT_XPATH, 
            XPaths.WHERE_FROM_INPUT_BOX_AFTER_INPUT_XPATH, self._where_from
        )

    @retry_if_exception_raised((TimeoutException, ElementNotInteractableException))
    def _input_where_to(self) -> None:
        self._input_to_text_box_with_update(
            XPaths.WHERE_TO_INPUT_BOX_PRE_INPUT_XPATH, 
            XPaths.WHERE_TO_INPUT_BOX_AFTER_INPUT_XPATH, self._where_to
        )

    @retry_if_exception_raised((TimeoutException, ElementNotInteractableException))
    @wait_before_execute(wait_time_seconds = 0.75)
    def _input_departure_date(self) -> None:
        date_box = self._find_element_by_xpath_with_wait(XPaths.DEPARTURE_DATE_INPUT_BOX_PRE_INPUT_XPATH)
        date_box.click()
        date_box = self._find_element_by_xpath_with_wait(XPaths.DEPARTURE_DATE_INPUT_BOX_AFTER_INPUT_XPATH)
        self._select_all_in_input_box()
        date_box.send_keys(Keys.BACK_SPACE)
        date_box.send_keys(self._departure_date)
        self._departure_date_is_set = True

    @retry_if_exception_raised((TimeoutException, ElementNotInteractableException))
    def _input_return_date(self) -> None:
        if not self._input_departure_date:
            raise RuntimeError('Need to call _input_departure_date() before _input_return_date()')
        date_box = self._find_element_by_xpath_with_wait(XPaths.RETURN_DATE_INPUT_BOX_PRE_INPUT_XPATH)
        date_box.click()
        self._select_all_in_input_box()
        date_box.send_keys(Keys.BACK_SPACE)
        date_box.send_keys(self._return_date)
        self._return_date_is_set = True

    @retry_if_exception_raised((TimeoutException, ElementNotInteractableException))
    def _click_done(self) -> None:
        if not self._return_date_is_set:
            raise RuntimeError('Need to call _input_return_date() before _click_done()')
        self._find_element_by_xpath_and_click(XPaths.DONE_X_PATH)

    @retry_if_exception_raised((TimeoutException, ElementNotInteractableException, HTMLNotFoundError))
    @wait_before_execute(wait_time_seconds = 0.25)
    def _click_more_flights(self) -> None:
        max_more_flights_list_elements = 20
        for i in range(1, max_more_flights_list_elements):
            try:
                self._find_element_by_xpath_and_click(XPaths.MORE_FLIGHTS_BUTTON_X_PATH_TEMPALTE.format(i), timeout_time_seconds = 1)
                self._found_more_flights_button = True
                return
            except TimeoutException:
                continue
        raise HTMLNotFoundError('more flights')

    @retry_if_exception_raised((TimeoutException, ElementNotInteractableException))
    @wait_before_execute(wait_time_seconds = 2)
    def _get_flight_data(self) -> pd.DataFrame:
        best_flights_data_string = self._try_get_best_flights_data_string()
        more_flights_data_string = self._try_get_more_flights_data_string()
        return self._data_parser.parse([best_flights_data_string, more_flights_data_string], self._departure_date, self._return_date)

    def _try_get_flight_data_string(self, x_path: str, flight_type: str) -> str:
        try:
            return self._find_element_by_xpath_with_wait(x_path).text
        except Exception:
            self._print_could_not_find_flights(flight_type)
            return ''

    def _print_could_not_find_flights(self, flight_type: str) -> None:
        print(f'Could not find {flight_type} flights for {self._where_from}, {self._where_to}, {self._departure_date}, {self._return_date}')

    def _try_get_best_flights_data_string(self) -> str:
        return self._try_get_flight_data_string(XPaths.BEST_FLIGHTS_X_PATH, 'best')

    def _try_get_more_flights_data_string(self) -> str:
        flight_type = 'more'
        if self._found_more_flights_button:
            return self._try_get_flight_data_string(XPaths.MORE_FLIGHTS_X_PATH, flight_type)
        self._print_could_not_find_flights(flight_type)
        return ''

    def _reset(self) -> None:
        self._departure_date_is_set = False
        self._return_date_is_set = False
        self._found_more_flights_button = False
        super()._reset()

    def _close(self) -> None:
        self._reset()
        super._close()

if __name__ == '__main__':
    pass