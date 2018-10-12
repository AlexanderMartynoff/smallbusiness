from os.path import dirname, abspath, join
from ruamel import yaml


APPLICATION_DIR = dirname(abspath(__file__))
RESOURCE_DIR = f'{APPLICATION_DIR}/_resource'
SQLITE3_DB = f'{RESOURCE_DIR}/database.sqlite3'


class Environment:
    _cache = {}

    def __init__(self, key):
        self._key = key
        self._working_dir = None
        self._parameter_path = None
        self._force_paths = None

    @classmethod
    def get(cls, key='__main__'):
        if key not in cls._cache:
            cls._cache[key] = cls(key)

        return cls._cache[key]

    def setup(self, working_dir, parameter_path, force_paths=()):
        self._working_dir = working_dir
        self._parameter_path = parameter_path
        self._force_paths = force_paths

        self._setup_parameter(self._parameter_path)
        self._setup_force_paths(self._force_paths)

        return self

    def _setup_parameter(self, path):
        with open(join(self._working_dir, path), 'rt') as file:
            self._parameter = yaml.load(file.read(), yaml.RoundTripLoader)

    def _setup_force_paths(self, paths):
        for path in paths:
            open(join(self._working_dir, path), 'a').close()

    def __getitem__(self, name):
        return self.parameter[name]

    @property
    def parameter(self):
        return self._parameter

    @property
    def ready(self):
        return all(self._working_dir, self._parameter_path, self._force_paths)
