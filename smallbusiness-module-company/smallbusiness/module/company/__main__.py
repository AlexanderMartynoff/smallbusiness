from smallbusiness.module.company import application, environment
from smallbusiness.framework.gunicorn import StandaloneApplication, options


if __name__ == '__main__':
    StandaloneApplication(application, {
        **options.__dict__,
        **environment['gunicorn']
    }).run()
