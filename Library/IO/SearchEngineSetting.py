from typing import Dict

class SearchEngineSetting:

    def __init__(self, search_engine_settings_dict: Dict[str, str]):
        try:
            self.name = search_engine_settings_dict['Name']
            self.base_url = search_engine_settings_dict['BaseURL']
        except KeyError as ex:
            raise ValueError(f'Search engine settings missing key {ex.args[0]}')

if __name__ == '__main__':
    pass
