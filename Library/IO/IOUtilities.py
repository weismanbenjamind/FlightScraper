from Library.Services import DatetimeService

def get_scrape_output_file_name():
    return f'ScrapeResults-{DatetimeService.get_current_date_and_time()}'

if __name__ == '__main__':
    pass