import six
import logging

from driver.connection import Connection
from driver.exceptions import *
from driver.protocol import *


log = logging.getLogger(__name__)


class Client(object):
    """
    Memcached client with connection pool
    """

    def __init__(self, server):
        self.server = server
        self.connection = Connection(server)
        self.connection.open()

    def close(self):
        self.connection.close()

    def set(self, key, value, expire=0, noreply=True):
        if not self.connection.socket:
            self.connection.open()

        flags = 0
        original_value = value

        if not isinstance(value, six.binary_type):
            try:
                value = _encode(value)
            except UnicodeEncodeError as e:
                raise DriverConversionException(
                        "Failed to convert value to binary with exception: %s" % str(e))

        arguments = b''
        if noreply:
            arguments += b' noreply'

        command = (b'set' +
                   b' ' + _encode(key) +
                   b' ' + _encode(flags) +
                   b' ' + _encode(expire) +
                   b' ' + _encode(len(value)) +
                   arguments + Constants.END_LINE +
                   value + Constants.END_LINE)

        try:
            self.connection.send(command)

            if noreply:
                return True

            return True
        except Exception as ex:
            log.error("Failed to send data %s with exception %s" % (original_value, str(ex)))
            log.error("Command failed: %s" % str(command))
            self.connection.close()
            pass


def _encode(data):
    return six.text_type(data).encode('ascii')