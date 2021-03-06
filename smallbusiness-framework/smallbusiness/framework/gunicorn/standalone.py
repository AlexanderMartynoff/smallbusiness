from gunicorn.app.base import BaseApplication


class StandaloneApplication(BaseApplication):

    def init(self, parser, opts, args):
        pass

    def __init__(self, application, options):
        self._application = application
        self._options = options

        super().__init__()

    def load_config(self):

        for key, value in self._options.items():
            if key in self.cfg.settings and value is not None:
                self.cfg.set(key.lower(), value)

    def load(self):
        return self._application
