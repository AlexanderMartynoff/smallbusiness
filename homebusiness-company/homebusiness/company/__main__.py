from homebusiness.framework.gunicorn import StandaloneApplication, options
from homebusiness.company import application


if __name__ == '__main__':
    StandaloneApplication(application, options.__dict__).run()
