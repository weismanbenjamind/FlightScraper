from Library.Webscrapers.GoogleFlightsWebscraper import GoogleFlightsWebscraper
from Library.Webscrapers.IWebscraper import IWebscraper
from Library.IO.SearchEngineSetting import SearchEngineSetting
from typing import Iterable

class WebscraperFactory:
    _WEBSCRAPER_MAP = {
        'GoogleFlights': GoogleFlightsWebscraper
    }

    def __init__(self, path_to_chromedriver) -> None:
        self._path_to_chromedriver = path_to_chromedriver

    def _create_webscraper(self, webscraper_name: str, base_url: str) -> IWebscraper:
        try:
            webscraper = self._WEBSCRAPER_MAP[webscraper_name]
        except KeyError:
            valid_webscrapers = ', '.join(sorted(self._webscraper_map.keys()))
            raise ValueError(f'Webscraper {webscraper_name} is invalid. Valid webscrapers are {valid_webscrapers}')

        try:
            return webscraper(base_url, self._path_to_chromedriver)
        except Exception as ex:
            raise Exception(f'Error instantiating webscraper {webscraper_name}') from ex

    def create_webscrapers(self, search_engine_settings: Iterable[SearchEngineSetting]):
        return [self._create_webscraper(search_engine_setting.name, search_engine_setting.base_url) for search_engine_setting in search_engine_settings]

if __name__ == '__main__':
    pass
