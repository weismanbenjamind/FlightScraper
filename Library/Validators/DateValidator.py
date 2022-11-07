from Library.Services.DatetimeService import DatetimeService
from datetime import datetime

class DateValidator:

    def __init__(self):
        self._delimiter = '-'
        self._current_date = ''
        self._current_day_of_week = ''

    def validate(self, date: str, day_of_week: str = '') -> None:
        self._current_date = date
        self._current_day_of_week = day_of_week
        self._validate_delimter_present()
        self._validate_date_format()
        if self._current_day_of_week:
            self._validate_day_of_week()
        self._current_date = ''
        self._current_day_of_week = ''

    def _validate_delimter_present(self):
        if self._delimiter not in self._current_date:
            raise ValueError(f'Expected {self._delimiter} to be in date: {self._current_date}')
    
    def _validate_date_format(self):
        actual_split = self._current_date.split(self._delimiter)
        target_split = ['MM', 'DD', 'YYYY']
        for actual_chars, target_chars_format in zip(actual_split, target_split):
            if len(actual_chars) != len(target_chars_format):
                target_format = self._delimiter.join(target_split)
                raise ValueError(f'Expected date {self._current_date} to have format {target_format}')

    def _validate_day_of_week(self):
        date = DatetimeService.mm_dd_yyyy_to_datetime(self._current_date)
        actual_day_of_week = DatetimeService.get_day_of_week(date)
        if actual_day_of_week != self._current_day_of_week:
            raise ValueError(f'Date {self._current_date} is {actual_day_of_week} and not {self._current_day_of_week}')

    @staticmethod
    def validate_day_of_week(datetime_obj: datetime, target_day_of_week: str):
        actual_day_of_week = DatetimeService.get_day_of_week(datetime_obj)
        if not actual_day_of_week != target_day_of_week:
            raise ValueError(f'Date of {datetime_obj} is a {actual_day_of_week}. Expected {target_day_of_week}')

if __name__ =='__main__':
    pass