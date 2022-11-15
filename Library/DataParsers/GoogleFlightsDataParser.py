
from Library.DataParsers.Decorators import flight_data_dict_validated
from Library.Exceptions.EmptyFlightDataStringError import EmptyFlightDataStringError
from typing import Iterable
import pandas as pd
import numpy as np
import re

class GoogleFlightsDataParser:
    _DEPARTURE_TIME = 'DepartureTime'
    _LANDING_TIME = 'LandingTime'
    _FLIGHT_LENGTH = 'FlightLength'
    _AIRPORTS = 'Airports'
    _NUM_STOPS = 'NumberStops'
    _PRICE_USD = 'Price(USD)'
    _DEPARTURE_DATE = 'DepartureDate'
    _RETURN_DATE = 'ReturnDate'

    _PRICE_UNAVAILABLE_PATTERN = r'[Pp]rice [Uu]navailable'

    def __init__(self, delimiter = '\n') -> None:
        self._delimiter = delimiter
        self._flight_data_string = ''
        self._flight_data_split = []
        self._departure_date = ''
        self._return_date = ''
        self._flight_data_dict = {
            self._RETURN_DATE: [],
            self._DEPARTURE_DATE: [],
            self._DEPARTURE_TIME: [],
            self._LANDING_TIME: [],
            self._FLIGHT_LENGTH: [],
            self._AIRPORTS: [],
            self._NUM_STOPS: [],
            self._PRICE_USD: [],
        }

    def parse(self, flight_data_strings: Iterable[str], departure_date: str, return_date: str) -> pd.DataFrame:
        try:
            self._initialize(flight_data_strings, departure_date, return_date)
        except EmptyFlightDataStringError:
            self._set_flight_data_dict_for_no_flight_data()
            return self._reset_and_get_flight_dataframe()
        self._get_deparute_and_landing_times()
        self._get_flight_lengths()
        self._get_airports()
        self._get_num_stops()
        self._get_prices()
        self._set_depart_and_return_dates()
        return self._reset_and_get_flight_dataframe()

    @flight_data_dict_validated
    def _get_flight_lengths(self) -> None:
        patterns = [
            r'\d?\d hr \d?\d min$',
            r'(\d\d hr )?\d?\d min$',
            r'\d?\d hr( \d?\d min)?$'
        ]
        self._iter_split_and_append_if_pattern_match(patterns, self._FLIGHT_LENGTH)

    @flight_data_dict_validated
    def _get_airports(self) -> None:
        airport_string_patterns = [r'[A-Z]{3}–[A-Z]{3}'] # Note the dash here is U+2013
        self._iter_split_and_append_if_pattern_match(airport_string_patterns, self._AIRPORTS)

    @flight_data_dict_validated
    def _get_num_stops(self) -> None:
        patterns = [
            r'Nonstop',
            r'\d{1,3} stop(s)?'
        ]
        self._iter_split_and_append_if_pattern_match(patterns, self._NUM_STOPS)

    @flight_data_dict_validated
    def _get_prices(self) -> None:
        patterns = [
            r'\$\d{1,5}(.\d{1,2})?',
            self._PRICE_UNAVAILABLE_PATTERN
        ]
        self._iter_split_and_append_if_pattern_match(patterns, self._PRICE_USD)
        self._prices_to_float()

    @flight_data_dict_validated
    def _get_deparute_and_landing_times(self) -> None:
        pattern = r'\d?\d:\d\d [PpAa][Mm]\+?\d?'
        times = re.findall(pattern, self._flight_data_string)
        self._validate_num_departure_and_return_times(len(times))
        self._append_departure_and_return_times_to_flight_data_dict(times)

    @flight_data_dict_validated
    def _set_depart_and_return_dates(self) -> None:
        max_datapoints = np.max([len(values) for values in self._flight_data_dict.values()])
        self._flight_data_dict[self._DEPARTURE_DATE] = [self._departure_date] * max_datapoints
        self._flight_data_dict[self._RETURN_DATE] = [self._return_date] * max_datapoints

    def _prices_to_float(self) -> None:
        prices = []
        sympbols_to_remove = ['$', ',']
        for price in self._flight_data_dict[self._PRICE_USD]:
            if re.match(self._PRICE_UNAVAILABLE_PATTERN, price):
                prices.append(np.NaN)
                continue
            else:
                for symbol in sympbols_to_remove:
                    price = price.replace(symbol, '')
                prices.append(float(price))
        self._flight_data_dict[self._PRICE_USD] = prices

    def _validate_num_departure_and_return_times(self, num_times: int) -> None:
        if  num_times % 2 != 0:
            raise ValueError(f'Found {num_times} times. Expected this value to be even')

    def _append_departure_and_return_times_to_flight_data_dict(self, times: Iterable[str]) -> None:
        for i, time in enumerate(times):
            if i % 2 == 0:
                self._append_to_flight_data_dict(self._DEPARTURE_TIME, time)
            else:
                self._append_to_flight_data_dict(self._LANDING_TIME, time)

    def _append_to_flight_data_dict(self, key: str, value: any) -> None:
        try:
            self._flight_data_dict[key].append(value)
        except KeyError as ex:
            raise Exception(f'Flight data dict does not have key {key}')

    def _iter_split_and_append_if_pattern_match(self, patterns: Iterable[str], field: str) -> None:
        if not self._flight_data_split:
            raise ValueError('Flight data dict empty')
        for datapoint in self._flight_data_split:
            for pattern in patterns:
                match = re.search(pattern, datapoint)
                if match:
                    self._append_to_flight_data_dict(field, datapoint)
                    break

    def _initialize(self, flight_data_strings: Iterable[str], departure_date: str, return_date: str) -> None:
        self._flight_data_string = self._delimiter.join(flight_data_strings)
        if not self._flight_data_string:
            raise EmptyFlightDataStringError()
        self._flight_data_split = self._flight_data_string.split(self._delimiter)
        self._departure_date = departure_date
        self._return_date = return_date

    @flight_data_dict_validated
    def _set_flight_data_dict_for_no_flight_data(self) -> None:
        self._flight_data_dict[self._DEPARTURE_DATE] = self._DEPARTURE_DATE
        self._flight_data_dict[self._RETURN_DATE] = self._RETURN_DATE
        target_keys = {self._RETURN_DATE, self._DEPARTURE_DATE}
        for key in self._flight_data_dict:
            if key not in target_keys:
                self._flight_data_dict[key] = np.NaN
    
    def _reset(self):
        self._flight_data_string = ''
        self._flight_data_split = []
        self._departure_date = ''
        self._return_date = ''
        self._flight_data_dict = {
            self._RETURN_DATE: [],
            self._DEPARTURE_DATE: [],
            self._DEPARTURE_TIME: [],
            self._LANDING_TIME: [],
            self._FLIGHT_LENGTH: [],
            self._AIRPORTS: [],
            self._NUM_STOPS: [],
            self._PRICE_USD: [],
        }

    def _reset_and_get_flight_dataframe(self) -> pd.DataFrame:
        flight_df = pd.DataFrame(self._flight_data_dict)
        self._reset()
        return flight_df

if __name__ == '__main__':
    pass