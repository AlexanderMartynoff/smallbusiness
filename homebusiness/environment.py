from os.path import dirname, abspath, join
from ruamel import yaml
from typing import Any, Dict, List, Optional


APPLICATION_DIR = dirname(abspath(__file__))
RESOURCE_DIR = f'{APPLICATION_DIR}/_resource'
SQLITE3_DB = f'{RESOURCE_DIR}/database.sqlite3'


class _Register:
    _register: Dict[str, Any]

    def __init__(self):
        self._register = {}

    def get(self, key, _type=None) -> Any:

        if key not in self._register.keys():
            self._register[key] = _Proxy()

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
    _implementation = None

    def __getattr__(self, name):
        if self._implementation is None:
            raise NotImplementedError('Service proxy has no implementation')

        return getattr(self._implementation, name)

    def _set_implementation(self, implementation):
        self._implementation = implementation

    @property
    def ready(self):
        return self._implementation is not None


class Environment:
    _cache = {}

    def __init__(self, key):
        self._key = key
        self._working_dir = None
        self._parameter_path = None
        self._force_paths = None
        self._register = _Register()

    @classmethod
    def get(cls, key='__main__'):
        if key not in cls._cache:
            cls._cache[key] = cls(key)

        return cls._cache[key]

    def setup(self, *,
              working_dir: str,
              parameter_path: str,
              force_paths: Optional[List[str]] = None,
              register_services: Optional[Dict[str, Any]] = None):

        self._working_dir = working_dir
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
        """ It should be call first """

        with open(join(self._working_dir, path), 'rt') as file:
            self._parameter = yaml.load(file.read(), yaml.RoundTripLoader)

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
