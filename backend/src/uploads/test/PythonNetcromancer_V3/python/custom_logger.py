import logging

def configure_logging():
    # Set the logging level
    logging.basicConfig(level=logging.INFO)

    # Create a file handler and set the logging level
    file_handler = logging.FileHandler('app.log')
    file_handler.setLevel(logging.ERROR)

    # Create a console handler and set the logging level
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)

    # Create a formatter and attach it to the handlers
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)

    # Get the root logger and add the handlers
    logger = logging.getLogger()
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

logger = logging.getLogger(__name__)

# Configure logging when this module is imported
#configure_logging()