from Library.Webscrapers.IWebscraper import IWebscraper
from Library.IO.Trip import Trip
from Library.Exceptions.MaxTripDateError import MaxTripDateError
import pandas as pd
from typing import Iterable
import time

class WebscrapeManager:

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
                    flight_data = pd.concat([flight_data, webscraper.scrape(**trip.get_search_settings())])
                    try:
                        trip.try_update()
                    except MaxTripDateError:
                        break
            webscraper.close()
        return flight_data

    def sleep(self) -> None:
        time.sleep(self._seconds_between_scrapes)

if __name__ == '__main__':
    pass
