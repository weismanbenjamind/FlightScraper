from Library.Factories.LoggerFactory import LoggerFactory
from Library.Webscrapers.IWebscraper import IWebscraper
from Library.IO.Trip import Trip
from Library.Exceptions.MaxTripDateError import MaxTripDateError
from typing import Iterable
from datetime import datetime
import pandas as pd
import time

class WebscrapeManager:

    _SORT_BY_COL = 'Price(USD)'

    def __init__(self, webscrapers: Iterable[IWebscraper], trips: Iterable[Trip], hours_between_scrapes: float) -> None:
        self._webscrapers = webscrapers
        self._trips = trips
        self._hours_between_scrapes = hours_between_scrapes
        self._seconds_between_scrapes = hours_between_scrapes * 60 * 60
        self._logger = LoggerFactory.try_create_logger(__name__)
        self._flight_data = pd.DataFrame()
        self._trip_settings = {}
        self._current_webscraper = None

    def scrape(self) -> pd.DataFrame:
        self._logger.info('Starting scrape')
        for webscraper in self._webscrapers:
            self._current_webscraper = webscraper
            self._current_webscraper.initialize_webdriver()
            for trip in self._trips:
                while True:
                    self._trip_settings = trip.get_search_settings()
                    trip_settings_string = self._get_trip_settings_string()
                    if trip.get_departure_date() < datetime.now():
                        self._logger.info(f'Trip {trip_settings_string} has departure date before current date - skipping trip')
                        if not trip.try_update():
                            break
                    else:
                        self._logger.info(f'Scraping for trip {trip_settings_string}')
                        try:
                            self._update_flight_data()
                            self._logger.info(f'Finished scraping flight data for trip {trip_settings_string}')
                        except Exception:
                            self._logger.exception(f'Error scraping flight data for trip {trip_settings_string}')
                        if not trip.try_update():
                            break
            webscraper.close()
            self._reset_trips()
        self._logger.info('Finished scrape')
        return self._get_flight_data_and_reset()

    def _reset_trips(self) -> None:
        for trip in self._trips:
            trip.reset()

    def _get_trip_settings_string(self) -> str:
        return ', '.join([f'{key}: {value}' for key, value in self._trip_settings.items()])

    def _update_flight_data(self) -> None:
        self._flight_data = pd.concat([self._flight_data, self._current_webscraper.scrape(**self._trip_settings)])

    def _get_flight_data_and_reset(self) -> pd.DataFrame:
        if (self._SORT_BY_COL) in self._flight_data.columns:
            self._flight_data.sort_values(by = self._SORT_BY_COL, inplace = True)
        flight_data_temp = self._flight_data.copy()
        self._reset()
        return flight_data_temp

    def _reset(self) -> None:
        self._flight_data = pd.DataFrame()
        self._trip_settings = {}
        self._current_webscraper = None

    def sleep(self) -> None:
        self._logger.info(f'Sleeping for {self._hours_between_scrapes} hours')
        time.sleep(self._seconds_between_scrapes)

if __name__ == '__main__':
    pass
