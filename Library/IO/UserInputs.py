from Library.IO.Trip import Trip
from typing import Dict, Union

class UserInputs:

    def __init__(self, user_inputs_dict: Dict[str, Union[str, int]]) -> None:
        try:
            trips = user_inputs_dict['Trips']
        except KeyError as ex:
            raise Exception(f'User inputs missing key {ex.args[0]}')

        self.trips = [Trip(trip) for trip in trips]

if __name__ == '__main__':
    pass