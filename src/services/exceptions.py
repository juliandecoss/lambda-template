from src.constants import DEFAULT_ERROR_MESSAGE
from src.services.error import get_error_code


class LambdaException(Exception):
    def __init__(
        self,
        status_code: int,
        internal_message: str = "",
        message: str = DEFAULT_ERROR_MESSAGE,
    ):
        self.status_code = status_code
        self.internal_message = internal_message
        self.message = message
        self.error_code = get_error_code(status_code, internal_message)
