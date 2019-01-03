from falcon.http_error import HTTPError
from falcon import status_codes, errors

from .logger import getlogger


logger = getlogger(__name__)


def httperror_handler(error, request, response, parameters):
    response.json = {'title': error.title}
    response.status = error.status


def exception_handler(error, request, response, parameters):
    response.json = {'title': status_codes.HTTP_500}
    response.status = status_codes.HTTP_500

    logger.exception(error)
