from os.path import isfile, join
from collections import Sequence
from ruamel import yaml


class Configurator:
    _config = None

    def __init__(self, dirs, name, autoload=True):
        self._names = [join(dir, name) for dir in dirs]
        
        if autoload:
            self._config, _name = self.load()

    def load(self):
        for name in self._names:
            if isfile(name):
                with open(name, 'rt') as file:
                    return yaml.load(file.read(), yaml.RoundTripLoader), name

    def __getitem__(self, name):
        if self._config is None:
            raise AttributeError('Maybe not loaded yet')

        return self._config[name]
