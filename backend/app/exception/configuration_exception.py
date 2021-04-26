class Error(Exception):
    """Base class for exceptions in this module."""
    pass


class ConfigurationException(Error):
    """Exception raised for errors in the configuration.

    Attributes:
        key -- configuration key which is affected
        message -- explanation of the error
    """

    def __init__(self, key, message):
        self.key = key
        self.message = message
