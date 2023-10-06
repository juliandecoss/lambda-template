from re import match

from src.constants import (
    DEFAULT_ERROR_CODE_CLIENT,
    DEFAULT_ERROR_CODE_SERVER,
    ERRORS_LOOKUP,
)


def get_error_code(status_code: int, error: str) -> int:
    errors_lookup = ERRORS_LOOKUP.get(status_code) or {}
    for key in errors_lookup.keys():
        if key in error:
            return errors_lookup[key]
    return (
        DEFAULT_ERROR_CODE_SERVER
        if match(r"5\d{2}", str(status_code))
        else DEFAULT_ERROR_CODE_CLIENT
    )
