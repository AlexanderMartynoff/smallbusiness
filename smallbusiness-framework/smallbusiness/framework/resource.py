from os.path import dirname, abspath, join, exists, isdir
from ruamel import yaml
from typing import Any, Dict, List, Optional, TextIO, ContextManager, Type, TypeVar, cast, Generic
from contextlib import contextmanager


T_co = TypeVar('T_co', contravariant=True)


FRAMEWORK_DIR = dirname(abspath(__file__))
FRAMEWORK_RESOURCE_DIR = FRAMEWORK_DIR + '/resource'
SQLITE_DB = FRAMEWORK_RESOURCE_DIR + '/database/application.sqlite'


class Resource:
    def __init__(self, paths: List[str]):
        self._paths = paths

    def load_settings(self, target: str, type='yaml') -> Dict[str, Any]:

        with self.open(target) as file:
            return yaml.load(file.read(), yaml.RoundTripLoader)

    @contextmanager
    def open(self, target, mode='rt') -> ContextManager[TextIO]:
        for path in self._paths:
            try:
                with open(join(path, target), mode) as file:
                    yield file
            except FileNotFoundError:
                pass
            else:
                return

        raise FileNotFoundError
