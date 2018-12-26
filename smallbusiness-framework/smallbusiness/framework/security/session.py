import json
from collections import MutableMapping

from falcon import Response, Request


class Session(dict):
    pass


class SessionStorage:

    def write(self, request: Request, response: Response, session):
        raise NotImplementedError

    def read(self, request: Request, response: Response):
        raise NotImplementedError


class CockieSessionStorage(SessionStorage):
    def __init__(self, coockie_name='falconsession', decode=json.loads, encode=json.dumps):
        self._coockie_name = coockie_name
        self._encode = encode
        self._decode = decode

    def read(self, request, response) -> Session:
        if self._coockie_name in request.cookies:
            return self._decode(request.cookies[self._coockie_name])

    def write(self, request, response, session: Session):
        response.set_cookie(self._coockie_name, self._encode(session), path='/', secure=False)


class SessionMiddleware:
    def __init__(self, session_storage: SessionStorage):
        self._session_storage = session_storage

    def process_request(self, request, response):
        if 'session' not in request.context:
            request.context['session'] = self._session_storage.read(request, response) or Session()
        else:
            raise KeyError('Key ``session`` already present in request context')

    def process_response(self, request, response, resource, succeeded):
        if 'session' in request.context:
            self._session_storage.write(request, response, request.context['session'])
        else:
            raise KeyError('Key `session` not present in request context')
