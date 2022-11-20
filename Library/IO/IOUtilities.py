from Library.Services import DatetimeService
import os

def get_scrape_output_file_path():
    output_dir = 'ScrapeResults'
    try:
        os.makedirs(output_dir)
    except FileExistsError:
        pass
    return os.path.sep.join(
        [
            output_dir,
            f'ScrapeResults-{DatetimeService.get_date_hours_minutes_seconds_mircroseconds()}'
        ]
    )

if __name__ == '__main__':
    pass