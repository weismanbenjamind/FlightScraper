from typing import Dict, Union
from Library.Validators.DateValidator import DateValidator

class Trip:

    def __init__(self, trip_dict: Dict[str, Union[str, int]]) -> None:
        try:
            self.where_to = trip_dict['WhereTo']
            self.where_from = trip_dict['WhereFrom']
            self.departure_day = trip_dict['DepartureDay']
            self.returning_day = trip_dict['ReturningDay']
            self.departure_date = trip_dict['DepartureDate']
        except KeyError as ex:
            raise Exception(f'Trip missing key {ex.args[0]}')

        try:
            DateValidator().validate(self.departure_date, self.departure_day)
        except Exception as ex:
            raise Exception(f'Date error with trip to {self.destination}')

if __name__ == '__main__':
    pass