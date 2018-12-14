from os.path import dirname, abspath, join, exists
from ruamel import yaml
from typing import Any, Dict, List, Optional, TextIO, ContextManager, Type, TypeVar, cast
from contextlib import contextmanager

T = TypeVar('T')


FRAMEWORK_DIR = dirname(abspath(__file__))
FRAMEWORK_RESOURCE_DIR = FRAMEWORK_DIR + '/resource'
SQLITE_DB = FRAMEWORK_RESOURCE_DIR + '/database.sqlite3'


class _Register:
    _register: Dict[str, Any]

    def __init__(self):
        self._register = {}

    def get(self, key, proxy: bool = False) -> Any:

        if key not in self._register.keys():
            if proxy:
                self._register[key] = _Proxy()
            else:
                raise KeyError(f'Service by key `{key}` not found in the register')

        return self._register[key]

    def set(self, key, value):
        service = self._register.get(key, None)

        if service is None:
            self._register[key] = value
        elif isinstance(service, _Proxy):
            if service.ready:
                raise ValueError('Service proxy already has implementation')
            else:
                service._set_implementation(value)
        else:
            raise ValueError('Service instance already setup')

        self._register[key] = {
            'value': value,
            'type': type(value),
        }


class _Proxy:
    _implementation: Any = None

    def __getattr__(self, name):
        if self._implementation is None:
            raise NotImplementedError('Service proxy has no implementation')

        return getattr(self._implementation, name)

    def _set_implementation(self, implementation: Any):
        self._implementation = implementation

    @property
    def ready(self):
        return self._implementation is not None


class Environment:
    _cache = {}

    def __init__(self, key):
        self._key = key
        self._working_dirs = None
        self._parameter_path = None
        self._force_paths = None
        self._register = _Register()

    @classmethod
    def get(cls, key='__main__'):
        if key not in cls._cache:
            cls._cache[key] = cls(key)

        return cls._cache[key]

    def setup(self, *,
              working_dirs: List[str],
              parameter_path: str,
              force_paths: Optional[List[str]] = None,
              register_services: Optional[Dict[str, Any]] = None):

        self._working_dirs = working_dirs
        self._parameter_path = parameter_path
        self._force_paths = force_paths
        self._register_services = register_services

        self._setup_parameter(self._parameter_path)

        if self._force_paths is not None:
            self._setup_force_paths(self._force_paths)

        if self._register_services is not None:
            self._setup_register(register_services)

        return self

    def _setup_parameter(self, path):
        """ This should called first """

        with self.open_resource(path) as file:
            self._parameter = yaml.load(file.read(), yaml.RoundTripLoader)

    @contextmanager
    def open_resource(self, path, mode='rt') -> ContextManager[TextIO]:
        for working_dir in self._working_dirs:
            try:
                with open(join(working_dir, path), mode) as file:
                    yield file
            except FileNotFoundError:
                pass
            else:
                return

        raise FileNotFoundError

    def _setup_register(self, services):
        for key, value in services.items():
            self._register.set(key, value)

    def _setup_force_paths(self, paths):
        for path in paths:
            open(join(self._working_dir, path), 'a').close()

    def __getitem__(self, name):
        return self.parameter[name]

    @property
    def parameter(self):
        return self._parameter

    @property
    def register(self):
        return self._register

    @property
    def ready(self):
        return all(self._working_dir, self._parameter_path, self._force_paths)
