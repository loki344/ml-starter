class Error(Exception):
    """Base class for exceptions in this module."""
    pass


class ConfigurationException(Error):
    """Exception raised for errors in the configuration."""

    def __init__(self, key: str, message: str):
        """
        Initializes a ConfigurationException

        :param key: configuration key which is affected
        :type key: str

        :param message: explanation of the error
        :type message: str
        """
        self.key = key
        self.message = message
