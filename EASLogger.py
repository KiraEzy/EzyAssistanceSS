import logging

class EASloggerSingleton:
    instance = None
    def __init__(self):
        self._logger = logging.getLogger(__name__)

    @staticmethod
    def getInstance():
        if EASloggerSingleton.instance is None:
            EASloggerSingleton.instance = EASloggerSingleton()
        return EASloggerSingleton.instance

    def info(self, filename, msg):
        # Create a logger
        logger = self.getInstance()._logger

        # Set the log level
        logger.setLevel(logging.INFO)

        # Create a file handler
        file_handler = logging.FileHandler('./logs/log_test.txt')
        # file_handler = logging.FileHandler(filename)

        # Set the formatter
        # formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        # file_handler.setFormatter(formatter)

        # Add the file handler to the logger
        if len(logger.handlers) == 0:
            logger.addHandler(file_handler)
        # Log some messages
        logger.info(msg.encode("utf-8"))

