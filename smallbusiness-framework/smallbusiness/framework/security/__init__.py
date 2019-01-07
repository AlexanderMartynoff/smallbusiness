from typing import Any, Dict, Union, Optional
from falcon import Response, Request

from .authentication import *
from .authorization import *
from .session import *
from .permission import haspermission


class SecurityServer:

    def __init__(self, authentication: AuthenticationPolicy,
                 authorization: AuthorizationPolicy):

        self._authentication = authentication
        self._authorization = authorization

    def put_context(self, context: Dict[str, Any],
                    request: Request,
                    response: Response):
        """ Put into session user context """

        assert 'session' in request.context, \
            RuntimeError('Expect key ``session`` in ``request.context``')

        request.context['session'][self._authentication.name] = self._authentication.encode(context)

    def get_context(self, request, response) -> Optional[Dict[str, Any]]:
        """ Get from session user identity """

        if self._authentication.name in request.context['session']:
            try:
                return self._authentication.decode(request.context['session'][self._authentication.name])
            except KeyError as error:
                pass

        return None

    @property
    def authorization(self):
        return self._authorization


class SecurityMiddleware:
    def __init__(self, server: SecurityServer):
        self._server = server

    def process_request(self, request: Request, response: Response):
        request.context['security'] = self._server
