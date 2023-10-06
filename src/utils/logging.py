from datetime import datetime
from json import dumps
from time import time_ns
from typing import Optional

from src.utils.helpers import camel_case_dict, get_case_insensitive_key


def logger(
    event: dict,
    *,
    extra_data: Optional[dict] = None,
    level: str = "",
    message: str = "",
    reason: str = None,
    request_id: str = "",
    start_time: int = 0,
    status_code: int = 200,
    token_data: Optional[dict] = None,
) -> None:
    headers = event.get("headers") or {}
    request_context = event.get("requestContext") or {}
    context_identity = request_context.get("identity") or {}
    common_data = token_data or {}
    display_name = common_data.get("display_name")
    if not display_name:
        display_name = (
            f'{common_data.get("name", "")} {common_data.get("custom:paternal_last_name", "")} {common_data.get("custom:maternal_last_name", "")}'
        ).strip()
    if not level:
        level = "SUCCESS" if 200 <= status_code < 400 else "ERROR"
    log_message = {
        "timestamp": str(datetime.now()),
        "network": {
            "device_mfa": get_case_insensitive_key(headers, "DEVICE_MFA"),
            "host": get_case_insensitive_key(headers, "host"),
            "origin": get_case_insensitive_key(headers, "origin"),
            "platform_origin": get_case_insensitive_key(headers, "Source-Origin")
            or get_case_insensitive_key(headers, "PLATFORM-ORIGIN"),
            "referer": headers.get("referer"),
            "request_id": request_context.get("requestId"),
            "source_ip": headers.get("true-client-ip")
            or context_identity.get("sourceIp"),
            "user_agent": context_identity.get("userAgent"),
            "X-Forwarded-For": headers.get("X-Forwarded-For"),
            "X-Forwarded-Port": headers.get("X-Forwarded-Port"),
            "X-Forwarded-Proto": headers.get("X-Forwarded-Proto"),
        },
        "request_id": request_id,
        "path": request_context.get("path"),
        "stage": request_context.get("stage"),
        "status_code": status_code,
        "level": level,
        "duration": (time_ns() - start_time) // 1000000 if start_time > 0 else None,
        "message": message,
    }
    if extra_data:
        log_message["extra_data"] = extra_data
    if reason:
        log_message["reason"] = reason
    print(dumps(camel_case_dict(log_message)))
