from Library.Services import DatetimeService
import logging
import os

class LoggerFactory:

    def __init__(self) -> None:
        self._log_file_parent_dir = 'Logs'

    def set_logging_settings(self):
        json_logging_format = '{Time: %(asctime)s, LogLevel: %(levelname)s, Message: %(message)s},'
        try:
            self._create_log_file_directory()
            logging.basicConfig(
                level = logging.DEBUG,
                format = json_logging_format,
                filename = self._get_log_file_path(),
                force = True
            )
        except Exception as ex:
            raise Exception('Failed to set logging settings') from ex

    def _create_log_file_directory(self) -> None:
        try:
            os.makedirs(self._log_file_parent_dir)
        except FileExistsError:
            logging.debug('Log file directory already exists')

    def _get_log_file_path(self) -> str:
        return os.path.sep.join(
            [
                self._log_file_parent_dir, 
                f'Scrape_Log_{DatetimeService.get_current_date_and_time()}.log'
            ]
        )

    @staticmethod
    def try_create_logger(name: str):
        try:
            return logging.getLogger(name)
        except Exception as ex:
            raise Exception(f'Failed to create logger with name {name}') from ex

if __name__ =='__main__':
    pass