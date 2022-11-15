from Library.Validators.IFileValidator import IFileValidator
from typing import Dict, Any
import json

class JsonParser(IFileValidator):

    def __init__(self) -> None:
        super().__init__()

    def _validate_filepath(self, path_to_json: str) -> None:
        self._current_file_path = path_to_json
        self._throw_if_path_doesnt_exist()
        self._throw_if_not_file()
        self._throw_if_not_filetype('.json')
        self._current_file_path = ''

    def try_read_json(self, path_to_json: str) -> Dict[str, Any]:
        self._validate_filepath(path_to_json)
        try:
            with open(path_to_json) as json_in:
                return json.load(json_in)
        except json.JSONDecodeError as ex:
            raise RuntimeError(f'Syntax error in json file {path_to_json}') from ex
        except Exception as ex:
            raise RuntimeError(f'Error reading in json file {path_to_json}') from ex

    def validate(self) -> None:
        raise NotImplementedError('JsonParser does not have an implementation of IValidator.validate()')

if __name__ == '__main__':
    pass