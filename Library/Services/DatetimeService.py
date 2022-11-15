from datetime import datetime, timedelta

MM_DD_YYYY_DATETIME_CODE = '%m-%d-%Y'

def mm_dd_yyyy_to_datetime(mm_dd_yyyy_date: str) -> datetime:
    return datetime.strptime(mm_dd_yyyy_date, MM_DD_YYYY_DATETIME_CODE)

def datetime_to_mm_dd_yyyy(datetime_obj: datetime) -> str:
    return datetime_obj.strftime(MM_DD_YYYY_DATETIME_CODE)

def get_day_of_week(datetime_obj: datetime) -> str:
    week_datetime_code = '%A'
    return datetime_obj.strftime(week_datetime_code)

def add_days(datetime_obj: datetime, num_days: int) -> datetime:
    return datetime_obj + timedelta(days = num_days)

def get_days_between_dates(datetime_obj_1: datetime, datetime_obj_2: datetime) -> float:
    return abs((datetime_obj_1 - datetime_obj_2).days)

def get_current_date_and_time():
    CURRENT_DATE_AND_TIME_CODE = '%m-%d-%Y %H:%M'
    return datetime.now().strftime(CURRENT_DATE_AND_TIME_CODE)

def get_minutes_between_dates(datetime_1, datetime_2):
    return abs((datetime_1 - datetime_2).seconds / 60)

if __name__ == '__main__':
    pass