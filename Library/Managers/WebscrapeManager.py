from Library.Webscrapers.IWebscraper import IWebscraper
from Library.IO.Trip import Trip
from Library.Exceptions.MaxTripDateError import MaxTripDateError
from typing import List
import time

class WebscrapeManager:

    def __init__(self, webscrapers: List[IWebscraper], trips: List[Trip], hours_between_scrapes: float) -> None:
        self._webscrapers = webscrapers
        self._trips = trips
        self._hours_between_scrapes = hours_between_scrapes
        self._seconds_between_scrapes = hours_between_scrapes * 60 * 60

    def scrape(self) -> None:
        for webscraper in self._webscrapers:
            for trip in self._trips:
                while True:
                    webscraper.scrape(**trip.get_search_settings())
                    try:
                        trip.try_update()
                    except MaxTripDateError:
                        break

    def sleep(self) -> None:
        time.sleep(self._seconds_between_scrapes)

if __name__ == '__main__':
    pass
