#TODO:
    # See why long term trips are failing
    # Create way to email results
    # Create time manager (maybe decorator) to manage how frequently scrapes take place
    # Clean code
    # Add exceptions handling
    # Add logging
    # Combine exceptions with loggin to keep app going upon erroring out

from Library.Validators.CommandLineArgsValidator import CommandLineArgsValidator
from Library.IO.JsonParser import JsonParser
from Library.IO.Appsettings import Appsettings
from Library.IO.UserInputs import UserInputs
from Library.Factories.WebscraperFactory import WebscraperFactory
from Library.Managers.WebscrapeManager import WebscrapeManager
import argparse

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
        CommandLineArgsValidator.validate(args)
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

    # Instantiate webscrapers
    print('Instantiating webscraper')
    try:
        web_scraper_factory = WebscraperFactory(appsettings.path_to_chromedriver)
        webscrapers = web_scraper_factory.create_webscrapers(appsettings.search_engine_settings)
        webscrape_manager = WebscrapeManager(webscrapers, user_inputs.trips, appsettings.hours_between_scrapes)
    except Exception as ex:
        raise Exception('Error creating webscrapers') from ex

    # Cleanup objects that are no longer needed
    del arg_parser
    del args
    del json_parser
    del user_inputs
    del appsettings
    del web_scraper_factory
    del webscrapers

    # Scrape
    print('Scraping')
    while True:
        webscrape_manager.scrape().sort_values(by = 'Price(USD)').to_csv('flight_data.csv', index = False)
        webscrape_manager.sleep()

if __name__ == '__main__':
    main()