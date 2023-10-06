from json import loads
from re import search

from src.utils.helpers import get_case_insensitive_key, snake_case_dict


class Request:
    def __init__(self, request_params: dict):
        self.raw = request_params
        self.params = snake_case_dict(self.raw)

        """Headers"""
        self.headers = self.params["headers"]
        self.host = self.get_header("host")
        self.origin = self.get_header("origin", default="*")

        """Context parameters"""
        self.context = self.params["request_context"]
        self.authorizer_context = self.context.get("authorizer") or {}
        self.path = self.params.get("path") or self.context.get("path", "")
        self.stage = self.context["stage"]

        """Identity parameters"""
        self.identity_context = self.context.get("identity") or {}
        self.ip = self.get_header("true_client_ip") or self.identity_context.get(
            "source_ip", ""
        )
        self.user_agent = self.identity_context.get("user_agent")

        self.body = self._parse_body(self.params.get("body") or "{}")
        self.host_app = self._get_app_name_by_host()
        self.method = self.params.get("http_method") or {}
        self.origin_app = self._get_app_name_by_origin()
        self.origin_domain = self._get_domain_by_origin()
        self.origin_subdomain_app = self._get_app_name_by_origin(subdomain=True)
        self.path_params = self.params.get("path_parameters") or {}
        self.query_params = self.params.get("query_string_parameters") or {}

    def _parse_body(self, query: str) -> dict:
        return loads(query)

    def _get_app_name_by_domain(self, domain: str, subdomain: bool = False) -> str:
        app_name = ""
        if not subdomain:
            if search(r"^(http(s?)://)?(.*?\.)?konfio\.mx$", domain):
                app_name = "konfio"
        return app_name

    def _get_app_name_by_origin(self, subdomain: bool = False):
        return self._get_app_name_by_domain(self.origin)

    def _get_app_name_by_host(self):
        return self._get_app_name_by_domain(self.host)

    def _get_domain_by_origin(self) -> str:
        get_domain = search(r"^(http(s?)://)?(.+)$", self.origin)
        return get_domain.group(1) if get_domain else ""

    def get_header(self, key: str, default: str = "") -> str:
        return get_case_insensitive_key(self.headers, key) or default
