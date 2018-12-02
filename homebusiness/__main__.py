from homebusiness import application
from homebusiness.gunicorn import StandaloneApplication, options


if __name__ == '__main__':
    StandaloneApplication(application, options.__dict__).run()
