import jwt
from falcon import Response, Request

from .session import Session


class AuthenticationPolicy:
    def token(self):
        NotImplementedError

    @property
    def name(self):
        self.__class__.__name__


class JWTAuthenticationPolicy(AuthenticationPolicy):
    def __init__(self, secret: str):
        self._secret = secret

    def validate(self, request) -> bool:
        return False


class SecurityServer:

    def __init__(self, policy: AuthenticationPolicy, session: Session):
        self._policy = policy
        self._session = session

    def remember(self, identity: str, request: Request, response: Response):
        self._session.put(self._policy.name, self._policy.token(), request, response)

    def validate(self, request, response):
        return self._policy.validate(self._session.get(self._policy.name, request, response))

    @property
    def policy(self):
        return self._policy


class AuthenticationMiddleware:
    def __init__(self, security_server: SecurityServer):
        self._security_server = security_server

    def process_request(self, request, response):
        if self._security_server.validate(request, response):
            pass
