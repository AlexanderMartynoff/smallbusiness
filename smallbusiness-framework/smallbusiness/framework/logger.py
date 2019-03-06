import logging


LOGGER_FORMAT = '%(asctime)s - %(name)s:%(lineno)d - %(levelname)s - %(message)s'


def setup(handlername: str ='stream',
          level: str = 'debug',
          format: str = LOGGER_FORMAT):

    handler = logging.StreamHandler()
    level = logging.getLevelName(level.upper())  # type: ignore

    handler.setFormatter(logging.Formatter(format))
    logging.basicConfig(handlers=[handler], level=level)


def getlogger(*args, **kwargs):
    return logging.getLogger(*args, **kwargs)
