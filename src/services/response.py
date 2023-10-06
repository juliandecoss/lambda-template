from json import dumps
from typing import Union

from src.services.request import Request
from src.utils.helpers import camel_case_dict


class Response:
    def __init__(
        self,
        request_params: Union[Request, dict],
        *,
        message: str,
        status_code: int,
        extra_data: dict = None
    ):
        self.request = (
            Request(request_params)
            if isinstance(request_params, dict)
            else request_params
        )
        self.message = message
        self.status_code = status_code
        self.extra_data = extra_data or {}
        self.headers = {
            "Access-Control-Allow-Origin": self.request.origin,
            "Vary": "Origin",
            "Access-Control-Allow-Methods": "POST, OPTIONS",
            "Access-Control-Allow-Credentials": "true",
            "Content-Type": "application/json",
            "Cache-Control": "no-cache",
        }

    def create(self):
        body = {"message": self.message}
        if self.extra_data:
            self.extra_data.pop("message", None)
            body.update(camel_case_dict(self.extra_data))
        response = {
            "status_code": self.status_code,
            "is_base64_encoded": False,
            "body": dumps(body),
        }
        response["headers"] = self.headers
        return camel_case_dict(response)
