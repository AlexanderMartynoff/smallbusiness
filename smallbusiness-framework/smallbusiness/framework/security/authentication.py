from typing import Any
import jwt
from falcon import Response, Request


class AuthenticationPolicy:
    def encode(self, data: Any):
        NotImplementedError

    def decode(self, data: str):
        NotImplementedError

    @property
    def name(self):
        return self.__class__.__name__.lower()


class JWTAuthenticationPolicy(AuthenticationPolicy):
    def __init__(self, secret: str, algorithm: str = 'HS256'):
        self._secret = secret
        self._algorithm = algorithm

    def encode(self, data: Any) -> str:
        return jwt.encode(data, self._secret, algorithm=self._algorithm).decode()

    def decode(self, token: str) -> bool:
        return jwt.decode(token.encode(), self._secret, algorithms=[self._algorithm])
