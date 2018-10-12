from document_stream_api import application
from document_stream_gunicorn import StandaloneApplication, options


if __name__ == '__main__':
    StandaloneApplication(application, options.__dict__).run()
