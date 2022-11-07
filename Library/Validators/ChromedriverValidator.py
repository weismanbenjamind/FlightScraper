from Library.Validators.IFileValidator import IFileValidator

class ChromedriverValidator(IFileValidator):

    def __init__(self) -> None:
        super().__init__()

    def validate(self, path_to_chromedriver: str) -> None:
        self._current_file_path = path_to_chromedriver
        self._throw_if_path_doesnt_exist()
        self._throw_if_not_file()
        self._current_file_path = ''

if __name__ == '__main__':
    pass