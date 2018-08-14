from gunicorn.app.base import BaseApplication

from . import options


class StandaloneApplication(BaseApplication):

    def __init__(self, application, options):
        self.application = application
        self.options = options

        super().__init__()

    def load_config(self):

        for key, value in self.options.items():
            if key in self.cfg.settings and value is not None:
                self.cfg.set(key.lower(), value)

    def load(self):
        return self.application