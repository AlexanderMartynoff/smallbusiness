from typing import Dict, Any, Union, Type, Optional
import json
from collections import MutableMapping

from falcon import Response, Request


class SessionStorage:

    def write(self, request: Request, response: Response,
              session: Dict[str, Any]):
        raise NotImplementedError

    def read(self, request: Request, response: Response):
        raise NotImplementedError


class CockieSessionStorage(SessionStorage):
    def __init__(self, coockie_name='falconsession', decode=json.loads, encode=json.dumps):
        self._coockie_name = coockie_name
        self._encode = encode
        self._decode = decode

    def read(self, request: Request, response: Response) -> Optional[Dict[str, Any]]:
        if self._coockie_name in request.cookies:
            return self._decode(request.cookies[self._coockie_name])
        return None

    def write(self, request: Request, response: Response,
              session: Dict[str, Any], path: str = '/'):
        response.set_cookie(
            self._coockie_name,
            self._encode(session),
            path=path,
            secure=False,
            http_only=False
        )


class SessionMiddleware:
    def __init__(self, session_storage: SessionStorage):
        self._session_storage = session_storage

    def process_request(self, request: Request, response: Response):
        if 'session' not in request.context:
            request.context['session'] = self._session_storage.read(request, response) or {}
        else:
            raise KeyError('Key ``session`` already present in request context')

    def process_response(self, request: Request,
                         response: Response,
                         resource: Any, succeeded: bool):
        if 'session' in request.context:
            self._session_storage.write(request, response, request.context['session'])
        else:
            raise KeyError('Key ``session`` not present in request context')
