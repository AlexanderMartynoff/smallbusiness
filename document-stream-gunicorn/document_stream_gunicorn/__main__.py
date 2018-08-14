from document_stream_api import api
from document_stream_gunicorn import StandaloneApplication, options


if __name__ == '__main__':
    StandaloneApplication(api, options.__dict__).run()
