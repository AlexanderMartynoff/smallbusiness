from falcon import Response, Request


class Session:
    def put(self, key: str, value: str, request: Request, response: Response):
        raise NotImplementedError

    def get(self, key: str, request: Request, response: Response):
        raise NotImplementedError


class CockieSession(Session):
    def __init__(self, cockie_name='falconsession'):
        self._cockie_name = cockie_name

    def put(self, key: str, value: str, request: Request, response: Response):
        pass
        # response.set_cookie(key, value, path='/', secure=False)

    def get(self, key: str, request: Request, response: Response):
        pass
