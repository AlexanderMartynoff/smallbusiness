from smallbusiness.module.company import application, settings
from smallbusiness.framework.gunicorn import StandaloneApplication, options


if __name__ == '__main__':
    StandaloneApplication(application, {
        **options.__dict__,
        **settings['gunicorn']
    }).run()
