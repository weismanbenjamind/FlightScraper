import argparse
from Library.Validators.CommandLineArgsValidator import CommandLineArgsValidator
from Library.IO.JsonParser import JsonParser
from Library.IO.Appsettings import Appsettings
from Library.Factories.WebscraperFactory import WebscraperFactory
from Library.IO.UserInputs import UserInputs
import time

def main():

    # Parse command line arguments
    try:
        arg_parser = argparse.ArgumentParser()
        arg_parser.add_argument(
            '--user-inputs',
            '-u',
            default = 'UserInputs.json',
            help = 'Path to user inputs'
        )
        arg_parser.add_argument(
            '--appsettings',
            '-a',
            default='Settings//AppSettings.json',
            help = 'Path to appsettings'
        )
        args = arg_parser.parse_args()
    except Exception as ex:
        raise Exception('Error parsing command line arguments') from ex

    # Validate command line arguments
    print('Validating command line arguments')
    try:
        CommandLineArgsValidator(args).validate()
    except Exception as ex:
        raise Exception('Invalid command line arguments') from ex

    # Read in appsettings
    print('Reading in appsettings')
    json_parser = JsonParser()
    try:
        appsettings = Appsettings(json_parser.try_read_json(args.appsettings))
    except Exception as ex:
        raise Exception('Error creating appsettings') from ex

    # Read in user inputs
    try:
        user_inputs = UserInputs(json_parser.try_read_json(args.user_inputs))
    except Exception as ex:
        raise Exception('Error creating user inputs') from ex

    web_scraper_factory = WebscraperFactory()
    webscrapers = []

    print('Instantiating webscrapers')
    for search_engine_setting in appsettings.search_engine_settings:
        webscrapers.append(web_scraper_factory.create_webscraper(search_engine_setting.name, search_engine_setting.base_url, appsettings.path_to_chromedriver))

    print('Scraping')
    for webscraper in webscrapers:
        for trip in user_inputs.trips:
            webscraper.scrape(trip.where_from, trip.where_to, trip.departure_date, '12-01-2022')
        time.sleep(10)
        webscraper.close()

if __name__ == '__main__':
    main()