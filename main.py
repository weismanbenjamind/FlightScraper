#TODO:
    # Add better exception handling
    # Add logging
        # Get selenium to stop logging
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

    try:
        logger = LoggerFactory.try_create_logger(__name__)
    except Exception:
        logging.exception(f'Error creating logger in {__name__}')
        logging.critical('Exiting program')
        exit()

    logger.info('Initializing settings for webscraping')

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

    try:
        CommandLineArgsValidator.validate(args)
    except Exception:
        logger.exception('Invalid command line arguments')
        logger.critical('Exiting program')
        exit()

    json_parser = JsonParser()
    try:
        appsettings = Appsettings(json_parser.try_read_json(args.appsettings))
    except Exception:
        logger.exception('Error creating appsettings')
        logger.critical('Exiting program')
        exit()

    try:
        user_inputs = UserInputs(json_parser.try_read_json(args.user_inputs))
    except Exception:
        logger.exception('Error creating user inputs')
        logger.critical('Exiting program')
        exit()

    try:
        web_scraper_factory = WebscraperFactory(appsettings.path_to_chromedriver)
        webscrapers = web_scraper_factory.create_webscrapers(appsettings.search_engine_settings)
        webscrape_manager = WebscrapeManager(webscrapers, user_inputs.trips, appsettings.hours_between_scrapes)
    except Exception:
        logger.exception('Error creating webscrapers')
        logger.critical('Exiting program')
        exit()

    del arg_parser
    del args
    del json_parser
    del user_inputs
    del appsettings
    del web_scraper_factory
    del webscrapers

    # Scrape
    while True:
        logger.info('Starting Scrape')
        try:
            webscrape_manager.scrape().to_csv(IOUtilities.get_scrape_output_file_name(), index = False)
        except Exception:
            logger.exception('Failed webscrape')
        logger.info('Sleeping')
        webscrape_manager.sleep()

if __name__ == '__main__':
    main()