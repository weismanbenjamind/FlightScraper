from Library.Validators.DateValidator import DateValidator
from Library.Services.DatetimeService import DatetimeService
from Library.Exceptions.MaxTripDateError import MaxTripDateError
from typing import Dict, Union
from datetime import datetime

class Trip:

    def __init__(self, trip_dict: Dict[str, Union[str, int]]) -> None:
        try:
            self._where_to = trip_dict['WhereTo']
            self._where_from = trip_dict['WhereFrom']
            self._departure_day = trip_dict['DepartureDay']
            self._returning_day = trip_dict['ReturningDay']
            self._departure_date = trip_dict['InitialDepartureDate']
            self._return_date = trip_dict['InitialReturnDate']
            self._max_trip_date = trip_dict['MaxTripDate']
        except KeyError as ex:
            raise Exception(f'Trip missing key {ex.args[0]}')

        date_validator = DateValidator()
        try:
            date_validator.validate(self._departure_date, self._departure_day)
            date_validator.validate(self._return_date, self._returning_day)
            date_validator.validate(self._max_trip_date)
        except Exception as ex:
            raise Exception(f'Date error with trip to {self.destination}')

        self._departure_date = DatetimeService.mm_dd_yyyy_to_datetime(self._departure_date)
        self._return_date = DatetimeService.mm_dd_yyyy_to_datetime(self._return_date)
        self._trip_length = DatetimeService.get_days_between_dates(self._return_date, self._departure_date)
        self._max_trip_date = DatetimeService.mm_dd_yyyy_to_datetime(self._max_trip_date)

    def try_update(self) -> None:
        self._departure_date = DatetimeService.add_days(self._departure_date, 7)
        DateValidator.validate_day_of_week(self._departure_date, self._departure_day)
        self._validate_date_less_than_max_date(self._departure_date)
        self._return_date = DatetimeService.add_days(self._return_date, 7)
        DateValidator.validate_day_of_week(self._return_date, self._returning_day)
        self._validate_date_less_than_max_date(self._return_date)

    def _validate_date_less_than_max_date(self, date: datetime) -> None:
        if date > self._max_trip_date:
            raise MaxTripDateError(DatetimeService.datetime_to_mm_dd_yyyy(date), DatetimeService.datetime_to_mm_dd_yyyy(self._max_trip_date))

    def get_search_settings(self) -> Dict[str, str]:
        return {
            "where_from": self._where_from,
            "where_to": self._where_to,
            "departure_date": DatetimeService.datetime_to_mm_dd_yyyy(self._departure_date),
            "return_date": DatetimeService.datetime_to_mm_dd_yyyy(self._return_date)
        }

if __name__ == '__main__':
    pass