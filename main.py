#TODO:
    # Add better exception handling
    # Add logging
    # Multithread such that trips get searched for at the same time
    # See why long term trips are failing
        # LA flights currently fail - For some reason not entering Las Angeles
    # Find way to notify self of results

from Library.Factories.LoggerFactory import LoggerFactory
from Library.Validators.CommandLineArgsValidator import CommandLineArgsValidator
from Library.IO.JsonParser import JsonParser
from Library.IO.Appsettings import Appsettings
from Library.IO.UserInputs import UserInputs
from Library.Factories.WebscraperFactory import WebscraperFactory
from Library.Managers.WebscrapeManager import WebscrapeManager
from Library.IO import IOUtilities
import argparse
import logging

def main():

    logging.debug('Setting logger settings')
    try:
        LoggerFactory().set_logging_settings()
    except Exception:
        logging.exception('Failed to set logger settings')
        logging.critical('Exiting program')
        exit()

    logging.debug(f'Setting logger in {__name__}')
    try:
        logger = LoggerFactory.try_create_logger(__name__)
    except Exception:
        logging.exception('Error creating logger in main.py')
        logging.critical('Exiting program')
        exit()

    logger.info('Initializing settings for webscraping')

    logger.debug('Parsing command line arguments')
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
    except Exception:
        logger.exception('Error parsing command line arguments')
        logger.critical('Exiting program')
        exit()

    # Validate command line arguments
    logger.debug('Validating command line arguments')
    try:
        CommandLineArgsValidator.validate(args)
    except Exception:
        logger.exception('Invalid command line arguments')
        logger.critical('Exiting program')
        exit()

    # Read in appsettings
    logger.debug('Reading in appsettings')
    json_parser = JsonParser()
    try:
        appsettings = Appsettings(json_parser.try_read_json(args.appsettings))
    except Exception:
        logger.exception('Error creating appsettings')
        logger.critical('Exiting program')
        exit()

    # Read in user inputs
    logger.debug('Reading in user inputs')
    try:
        user_inputs = UserInputs(json_parser.try_read_json(args.user_inputs))
    except Exception:
        logger.exception('Error creating user inputs')
        logger.critical('Exiting program')
        exit()

    # Instantiate webscrapers
    logger.debug('Instantiating webscrapers')
    try:
        web_scraper_factory = WebscraperFactory(appsettings.path_to_chromedriver)
        webscrapers = web_scraper_factory.create_webscrapers(appsettings.search_engine_settings)
        webscrape_manager = WebscrapeManager(webscrapers, user_inputs.trips, appsettings.hours_between_scrapes)
    except Exception:
        logger.exception('Error creating webscrapers')
        logger.critical('Exiting program')

    # Cleanup objects that are no longer needed
    logger.debug('Cleaning up unused objects')
    del arg_parser
    del args
    del json_parser
    del user_inputs
    del appsettings
    del web_scraper_factory
    del webscrapers

    # Scrape
    while True:
        logger.info('Scraping')
        webscrape_manager.scrape().to_csv(IOUtilities.get_scrape_output_file_name(), index = False)
        logger.info('Sleeping')
        webscrape_manager.sleep()

if __name__ == '__main__':
    main()