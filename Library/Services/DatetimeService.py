import datetime

class DatetimeService:
    _MM_DD_YYYY_DATETIME_CODE = '%m-%d-%Y'

    @staticmethod
    def mm_dd_yyyy_to_datetime(mm_dd_yyyy_date: str) -> datetime.datetime:
        mm_dd_yyyy_datetime_code = '%m-%d-%Y'
        return datetime.datetime.strptime(mm_dd_yyyy_date, DatetimeService._MM_DD_YYYY_DATETIME_CODE)

    @staticmethod
    def datetime_to_mm_dd_yyyy(datetime_obj: datetime.datetime) -> str:
        return datetime_obj.strftime(DatetimeService._MM_DD_YYYY_DATETIME_CODE)
   
    @staticmethod
    def get_day_of_week(datetime_obj: datetime.datetime) -> str:
        week_datetime_code = '%A'
        return datetime_obj.strftime(week_datetime_code)

    @staticmethod
    def add_days(datetime_obj: datetime.datetime, num_days: int) -> datetime.datetime:
        return datetime_obj + datetime.timedelta(days = num_days)

    @staticmethod
    def get_days_between_dates(datetime_obj_1: datetime, datetime_obj_2: datetime) -> float:
        return abs((datetime_obj_1 - datetime_obj_2).days)

if __name__ == '__main__':
    pass