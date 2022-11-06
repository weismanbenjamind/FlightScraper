from typing import Any
from Library.Validators.IFileValidator import IFileValidator

class CommandLineArgsValidator(IFileValidator):

    def __init__(self, args: Any) -> None:
        self._args = args
        super().__init__()

    def validate(self):
        target_keys = [
            'user_inputs',
            'appsettings'
        ]
        for key in target_keys:
            try:
                filepath = getattr(self._args, key)
            except Exception as ex:
                raise ValueError(f'Expected args to have setting {key}')
            self._current_file_path = filepath
            self._throw_if_path_doesnt_exist()
            self._throw_if_not_file()
            self._throw_if_not_filetype('.json')
        self._current_file_path = ''

    def set_args(self, args: Any):
        self._args = args

if __name__ == '__main__':
    pass