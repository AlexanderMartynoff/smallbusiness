import re
import json
from typing import Dict, List, Union, Callable, AnyStr, Any

from falcon import response, request
from cached_property import cached_property
import sqlite3


CONTENT_TYPE_JSON = 'application/json'
CONTENT_TYPE_HTML = 'text/html'
ENCODING = 'utf-8'


re_camel_to_snake = re.compile(r'(?!^)(?<!_)([A-Z])')
re_snake_to_camel = re.compile(r'(?:_)(.)')


def _atom_snake_to_camel(string: str) -> str:
    return re_snake_to_camel.sub(lambda match: match.group(1).upper(), string)


def _atom_camel_to_snake(string: str) -> str:
    return re_camel_to_snake.sub(r'_\1', string).lower()


def convert_notation(data: Any, atom_mapper: Callable[[str], str], ignore_if_atom: bool = False) -> Any:

    if isinstance(data, dict):
        return {convert_notation(key, atom_mapper): convert_notation(
            value,
            atom_mapper,
            True
        ) for key, value in data.items()}

    elif isinstance(data, list):
        return [convert_notation(value, atom_mapper, True) for value in data]

    elif not ignore_if_atom and isinstance(data, str):
        return atom_mapper(data)

    return data


class Request(request.Request):
    @cached_property
    def json(self):
        return self._convert(json.loads(self.stream.read().decode(ENCODING)))

    def _convert(self, data: Any):
        return convert_notation(data, _atom_camel_to_snake)


class Response(response.Response):
    @property
    def json(self):
        return self.body

    @json.setter
    def json(self, value):
        self.content_type = CONTENT_TYPE_JSON
        self.body = json.dumps(self._convert(value), cls=JSONEncoder)

    def _convert(self, data):
        return convert_notation(data, _atom_snake_to_camel)


class JSONEncoder(json.JSONEncoder):

    def default(self, data):
        if isinstance(data, sqlite3.Row):
            return {key: data[key] for key in data.keys()}
        return data
