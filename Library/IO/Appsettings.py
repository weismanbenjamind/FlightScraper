from Library.IO.SearchEngineSetting import SearchEngineSetting
from Library.Validators.ChromedriverValidator import ChromedriverValidator
from typing import Dict, Union, List

class Appsettings():

    def __init__(self, appsettings_dict: Dict[str, Union[str, List[Dict[str, str]]]]) -> None:
        try:
            self.path_to_chromedriver = appsettings_dict['PathToChromeDriver']
            self.hours_between_scrapes = appsettings_dict['HoursBetweenScrapes']
            self.search_engine_settings = appsettings_dict['SearchEngineSettings']
        except KeyError as ex:
            raise Exception(f'Appsettings missing value for {ex.args[0]}')

        try:
            ChromedriverValidator().validate(self.path_to_chromedriver)
        except Exception as ex:
            Exception(f'Invalid path to chromedriver: {self.path_to_chromedriver}')

        try:
            self.search_engine_settings = [SearchEngineSetting(setting) for setting in self.search_engine_settings]
        except Exception as ex:
            raise Exception('Error creating search engine settings') from ex

if __name__ == '__main__':
    pass
