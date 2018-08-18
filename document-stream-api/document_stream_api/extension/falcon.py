import json
import falcon
from falcon import response, request
from falcon.status_codes import *
from falcon.errors import HTTPNotFound
from cached_property import cached_property

from .json import JSONEncoder


CONTENT_TYPE_JSON = 'application/json'
CONTENT_TYPE_HTML = 'text/html'
DEFAULT_ENCONDING = 'utf-8'


class API(falcon.API):
    def add_route(self, uri_templates, resource, *args, **kwargs):
        if not isinstance(uri_templates, (tuple, set, list)):
            uri_templates = [uri_templates]

        for uri_template in uri_templates:
            super().add_route(uri_template, resource, *args, **kwargs)


class Request(request.Request):
    @cached_property
    def json(self):
        return json.loads(self.stream.read().decode(DEFAULT_ENCONDING))


class Response(response.Response):
    @property
    def json(self):
        return self.body

    @json.setter
    def json(self, value):
        self.content_type = CONTENT_TYPE_JSON
        self.body = json.dumps(value, cls=JSONEncoder)
