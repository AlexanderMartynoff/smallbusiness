from typing import Any
from falcon import Response, Request

from .authentication import *
from .session import *


class SecurityServer:

    def __init__(self, policy: AuthenticationPolicy):
        self._policy = policy

    def put(self, identity: str, request: Request, response: Response):
        request.context['session'][self._policy.name] = self._policy.encode({'identity': identity})

    def get(self, request, response):
        if self._policy.name in request.context['session']:
            try:
                return self._policy.decode(request.context['session'][self._policy.name])
            except Exception as error:
                pass


class SecurityMiddleware:
    def __init__(self, security_server: SecurityServer):
        self._security_server = security_server

    def process_request(self, request: Request, response: Response):
        request.context['security'] = self._security_server.get(request, response)
