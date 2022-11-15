#TODO:
    # See why long term trips are failing
        # LA flights currently fail - For some reason not entering Las Angeles
    # Clean code
    # Add exception handling
        # Fix hack with more flights currently in place
    # Add logging
    # Combine exceptions with logging to keep app going upon erroring out
    # Find way to notify self of results

from Library.Validators.CommandLineArgsValidator import CommandLineArgsValidator
from Library.IO.JsonParser import JsonParser
from Library.IO.Appsettings import Appsettings
from Library.IO.UserInputs import UserInputs
from Library.Factories.WebscraperFactory import WebscraperFactory
from Library.Managers.WebscrapeManager import WebscrapeManager
from Library.IO import IOUtilities
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
    print('Instantiating webscrapers')
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
    while True:
        print('Scraping')
        webscrape_manager.scrape().to_csv(IOUtilities.get_scrape_output_file_name(), index = False)
        print('Sleeping')
        webscrape_manager.sleep()

if __name__ == '__main__':
    main()