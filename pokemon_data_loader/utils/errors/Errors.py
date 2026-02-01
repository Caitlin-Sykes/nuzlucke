import logging

# Initialize a standalone logger for the errors module
logger = logging.getLogger("errors")

class PokeAPIError(Exception):
    """PokeAPI communication errors."""
    def __init__(self, message, status_code=None):
        super().__init__(message)
        logger.error(message)
        self.status_code = status_code

class FailedToCreateAbilityError(Exception):
    """An error raised when an ability cannot be created."""
    def __init__(self, message, status_code=None):
        super().__init__(message)
        logger.error(message)
