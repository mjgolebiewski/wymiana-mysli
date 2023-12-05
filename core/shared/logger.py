import logging


class LoggerSingleton:
    """
    A simple logger for PyFlink applications.
    """

    _instance = None

    def __new__(cls, logger_name="LoggerSingleton", log_level=logging.INFO):
        if cls._instance is None:
            cls._instance = super(LoggerSingleton, cls).__new__(cls)
            cls._instance.logger = logging.getLogger(logger_name)
            cls._instance.logger.setLevel(log_level)
            cls._instance._setup_logging()
        return cls._instance

    def _setup_logging(self) -> None:
        """
        Configures the logger with a stream handler and a formatter.
        """
        ch = logging.StreamHandler()
        ch.setLevel(logging.DEBUG)

        formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        )
        ch.setFormatter(formatter)
        self.logger.addHandler(ch)

    def info(self, message: str) -> None:
        """
        Logs a message with log level INFO.

        Parameters:
        ----------
        message : str
            The message to log.
        """
        self.logger.info(message)

    def debug(self, message: str) -> None:
        """
        Logs a message with log level DEBUG.

        Parameters:
        ----------
        message : str
            The message to log.
        """
        self.logger.debug(message)

    def error(self, message: str) -> None:
        """
        Logs a message with log level ERROR.

        Parameters:
        ----------
        message : str
            The message to log.
        """
        self.logger.error(message)

    def warning(self, message: str) -> None:
        """
        Logs a message with log level WARNING.

        Parameters:
        ----------
        message : str
            The message to log.
        """
        self.logger.warning(message)

    def critical(self, message: str) -> None:
        """
        Logs a message with log level CRITICAL.

        Parameters:
        ----------
        message : str
            The message to log.
        """
        self.logger.critical(message)
