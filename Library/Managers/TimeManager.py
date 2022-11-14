from Library.Services.DatetimeService import DatetimeService
from time import time
from typing import List
from datetime import datetime

class TimeManager:

    def __init__(self, scrape_times: List[datetime], scrape_time_error_minutes: float, sleep_time_minutes: float):
        self._scrape_times = scrape_times
        self._scrape_time_error_minutes = scrape_time_error_minutes
        self._sleep_time_minutes = sleep_time_minutes
        self._validate_scrape_times()

    def _validate_scrape_times(self):
        for i in range(len(self._scrape_times.sort()) - 1):
            scrape_time_diff_minutes = DatetimeService.get_minutes_between_dates(self._scrape_times[i+1], self._scrape_times[i])
            if scrape_time_diff_minutes <= self._sleep_time_minutes:
                raise RuntimeError(
                    f'Scrape time diff of {scrape_time_diff_minutes} minutes is '
                    f'less than or equal to sleep time of {self._scrape_time_minutes} minutes'
                )

    def is_scrape_time(self):
        for datetime_obj in self._scrape_times:
            now_datetime_obj = datetime.now()
            if DatetimeService.get_minutes_between_dates(datetime_obj, now_datetime_obj) <= self._scrape_time_error_minutes:
                return True

    def sleep(self):
        time.sleep(self._sleep_time_minutes * 60)

if __name__ == '__main__':
    pass
