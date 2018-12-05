from homebusiness.framework import application
from homebusiness.framework.gunicorn import StandaloneApplication, options


if __name__ == '__main__':
    StandaloneApplication(application, options.__dict__).run()
