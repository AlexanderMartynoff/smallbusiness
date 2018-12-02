from document_stream import application
from document_stream.gunicorn import StandaloneApplication, options


if __name__ == '__main__':
    StandaloneApplication(application, options.__dict__).run()
