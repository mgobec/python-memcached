import logging


class NullHandler(logging.Handler):

    def emit(self, record):
        pass

logging.getLogger('driver').addHandler(NullHandler())

