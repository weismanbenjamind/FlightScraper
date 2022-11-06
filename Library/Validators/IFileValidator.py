from os import path

class IFileValidator:

    def __init__(self) -> None:
        self._current_file_path = ''

    def _throw_if_path_doesnt_exist(self) -> None:
        if not path.exists(self._current_file_path):
            raise FileNotFoundError(f'Filepath {self._current_file_path} doesn\'t exist')

    def _throw_if_not_file(self) -> None:
        if not path.isfile(self._current_file_path):
            raise OSError(f'Filepath {self._current_file_path} does not lead to a file')

    def _throw_if_not_filetype(self, filetype: str) -> None:
        if not self._current_file_path.endswith(filetype):
            raise OSError(f'Expected filepath {self._current_file_path} to lead to a {filetype} file')

    def validate(self):
        raise NotImplementedError('IValidator.validate() is a virtual method and must be overriden')

    def set_current_file_path(self, filepath: str) -> None:
        self._current_file_path = filepath

if __name__ == '__main__':
    pass