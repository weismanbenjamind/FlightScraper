from typing import Callable

def flight_data_dict_validated(func: Callable) -> Callable:
    def wrapper(*args, **kwargs):
        func(*args, **kwargs)
        _self = args[0]
        flight_data_dict_attribute = '_flight_data_dict'
        if not hasattr(_self, '_flight_data_dict'):
            raise AttributeError(
                'flight_data_dict_validated decorator expects passed function '
                'to have a self argument with attribute '
                f'{flight_data_dict_attribute}'
            )
        for field_1, col_vals_1 in _self._flight_data_dict.items():
            num_datapoints_1 = len(col_vals_1)
            if num_datapoints_1 == 0:
                continue
            for field_2, col_vals_2 in _self._flight_data_dict.items():
                num_datapoints_2 = len(col_vals_2)
                if num_datapoints_2 == 0:
                    continue
                if num_datapoints_1 != num_datapoints_2:
                    raise ValueError(
                        f'Field {field_1} has {num_datapoints_1} datapoints '
                        f'while field {field_2} has {num_datapoints_2}'
                    )
    return wrapper

if __name__ == '__main__':
    pass