from Library.Webscrapers.IWebscraper import IWebscraper
from Library.IO.Trip import Trip
from Library.Exceptions.MaxTripDateError import MaxTripDateError
import pandas as pd
from typing import Iterable
import time

class WebscrapeManager:

    _SORT_BY_COL = 'Price(USD)'

    def __init__(self, webscrapers: Iterable[IWebscraper], trips: Iterable[Trip], hours_between_scrapes: float) -> None:
        self._webscrapers = webscrapers
        self._trips = trips
        self._hours_between_scrapes = hours_between_scrapes
        self._seconds_between_scrapes = hours_between_scrapes * 60 * 60

    def scrape(self) -> pd.DataFrame:
        flight_data = pd.DataFrame()
        for webscraper in self._webscrapers:
            webscraper.initialize_webdriver()
            for trip in self._trips:
                while True:
                    try:
                        flight_data = pd.concat([flight_data, webscraper.scrape(**trip.get_search_settings())])
                    except Exception as ex:
                        trip_info = ', '.join([f'{key}: {value}' for key, value in trip.get_search_settings().items()])
                        print(f'\nError with trip {trip_info}\n{ex}\n')
                    try:
                        trip.try_update()
                    except MaxTripDateError:
                        break
            webscraper.close()
            self._trips = [trip.reset() for trip in self._trips]
        if (self._SORT_BY_COL) in flight_data.columns:
            flight_data.sort_values(by = self._SORT_BY_COL, inplace = True)
        return flight_data

    def sleep(self) -> None:
        time.sleep(self._seconds_between_scrapes)

if __name__ == '__main__':
    pass
