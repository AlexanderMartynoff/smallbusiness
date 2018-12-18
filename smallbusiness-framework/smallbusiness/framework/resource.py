from os.path import dirname, abspath, join, exists, isdir
from ruamel import yaml
from typing import Any, Dict, List, Optional, TextIO, ContextManager, Type, TypeVar, cast, Generic
from contextlib import contextmanager


T_co = TypeVar('T_co', contravariant=True)


FRAMEWORK_DIR = dirname(abspath(__file__))
FRAMEWORK_RESOURCE_DIR = FRAMEWORK_DIR + '/resource'
SQLITE_DB = FRAMEWORK_RESOURCE_DIR + '/database.sqlite3'


class Resource:
    def __init__(self, dirs: List[str]):
        self._dirs = dirs

    def load_yaml(self, path):

        with self.load(path) as file:
            return yaml.load(file.read(), yaml.RoundTripLoader)

    @contextmanager
    def load(self, path, mode='rt') -> ContextManager[TextIO]:
        for dir in self._dirs:
            try:
                with open(join(dir, path), mode) as file:
                    yield file
            except FileNotFoundError:
                pass
            else:
                return

        raise FileNotFoundError
