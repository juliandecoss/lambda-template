DEFAULT_ERROR_CODE_SERVER = 5000
DEFAULT_ERROR_MESSAGE = "Something went wrong"
DEFAULT_SERVER_ERROR_MESSAGE = "Internal server error"
DEFAULT_ERROR_CODE_CLIENT = 1000
HTTP_VERB_GET = "GET"
HTTP_VERB_POST = "POST"
ERRORS_LOOKUP = {
    400: {
        "Not supported path": 1001,
        "Missing field": 1002,
        "Schema registry error": 1003,
        "Publishing exception": 1004,
        "Not valid format headers": 1005,
        "Not a valid topic name": 1006,
        "Can't create connector": 1007,
    }
}
