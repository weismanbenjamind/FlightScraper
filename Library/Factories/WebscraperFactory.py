from Library.Webscrapers.GoogleFlightsWebscraper import GoogleFlightsWebscraper
from Library.Webscrapers.IWebscraper import IWebscraper

class WebscraperFactory:

    def __init__(self) -> None:
        self._webscraper_map = {
            'GoogleFlights': GoogleFlightsWebscraper
        }

    def create_webscraper(self, webscraper_name: str, base_url: str, path_to_chromedriver: str) -> IWebscraper:
        try:
            webscraper = self._webscraper_map[webscraper_name]
        except KeyError:
            valid_webscrapers = ', '.join(sorted(self._webscraper_map.keys()))
            raise ValueError(f'Webscraper {webscraper_name} is invalid. Valid webscrapers are {valid_webscrapers}')

        try:
            return webscraper(base_url, path_to_chromedriver)
        except Exception as ex:
            raise Exception(f'Error instantiating webscraper {webscraper_name}') from ex

if __name__ == '__main__':
    pass
