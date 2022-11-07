class MaxTripDateError(Exception):

    def __init__(self, current_date: str, max_trip_date: str) -> None:
        super().__init__(f'Date of {current_date} exceedes max trip date {max_trip_date}')

if __name__ == '__main__':
    pass