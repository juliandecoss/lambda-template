from json import loads
from time import time_ns
from traceback import print_exc

from src.constants import DEFAULT_SERVER_ERROR_MESSAGE, HTTP_VERB_GET, HTTP_VERB_POST
from src.services.exceptions import LambdaException
from src.services.request import Request
from src.services.response import Response
from src.utils.logging import logger


def main(event: dict, context) -> dict:
    try:
        log = {"request_id": context.aws_request_id, "start_time": time_ns()}
        request = Request(event)
        extra_data = {"info": "save extra info"}
        message = "successful lambda invokation"
        if request.path == "/something":
            if request.method == HTTP_VERB_GET:
                message = "successful lambda invokation by path"
        else:
            raise LambdaException(400, "Not supported path")
        response = Response(
            request, status_code=200, message=message, extra_data=extra_data
        ).create()
        logger(
            event=event,
            message=loads(response["body"])["message"],
            status_code=response["statusCode"],
            extra_data=extra_data,
            **log,
        )
        return response
    except LambdaException as e:
        print_exc()
        status_code = e.status_code
        message = e.message
        reason = e.internal_message
        error_data = {"code": e.error_code}
    except Exception as e:
        print_exc()
        status_code = 500
        message = DEFAULT_SERVER_ERROR_MESSAGE
        reason = f"{e.__class__.__name__}: {e}"
        error_data = {}
    logger(event=event, status_code=status_code, message=message, reason=reason, **log)
    return Response(
        event, status_code=status_code, message=message, extra_data=error_data
    ).create()