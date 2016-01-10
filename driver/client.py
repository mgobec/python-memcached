import six
import logging

from driver.connection import Connection
from driver.exceptions import *
from driver.protocol import *


log = logging.getLogger(__name__)


class Client(object):
    """
    Memcached client implementation
    """

    def __init__(self, server):
        self.server = server
        self.connection = Connection(server)
        self.connection.open()

    def close(self):
        self.connection.close()

    def get(self, key):
        if not self.connection.socket:
            self.connection.open()

        command = (b'get' +
                   b' ' + _encode(key) +
                   Constants.END_LINE)

        try:
            self.connection.send(command)
        except Exception as ex:
            log.error("Command failed: %s" % str(command), ex)
            self.connection.close()
            pass

        try:
            response = self.connection.read()
        except Exception as ex:
            log.error("Failed to read response from socket", ex)
            self.connection.close()
            pass

        log.debug("Received from socket: %s" % response)
        result = _parse_get_response(response)
        _check_for_errors(result[0])
        if len(result) > 2:
            return result[1]

        raise DriverUnknownException(
            "Received unexpected response from the memcached instance %s" % str(result))

    def set(self, key, value, expire=0, noreply=True):
        if not self.connection.socket:
            self.connection.open()

        if not isinstance(value, six.binary_type):
            try:
                value = _encode(value)
            except UnicodeEncodeError as e:
                raise DriverConversionException(
                        "Failed to convert value to binary with exception: %s" % str(e))

        flags = 0
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
        except Exception as ex:
            log.error("Command failed: %s" % str(command), ex)
            self.connection.close()
            pass

        if noreply:
            return True

        try:
            response = self.connection.read()
        except Exception as ex:
            log.error("Failed to read response from socket", ex)
            self.connection.close()
            pass

        log.debug("Received from socket: %s" % response)
        result = _parse_set_response(response)
        _check_for_errors(result)
        if result == StoreReply.STORED:
            log.debug("Successfully stored data")
            return True
        elif result == StoreReply.EXISTS:
            log.debug("Entry already exists")
            return False
        elif result == StoreReply.NOT_STORED:
            log.warn("Entry not stored for some reason")
            return False
        elif result == StoreReply.NOT_FOUND:
            log.warn("Received not found response")
            return False

        raise DriverUnknownException(
            "Received unexpected response from the memcached instance %s" % str(result))


def _encode(data):
    return six.text_type(data).encode('ascii')


def _parse_set_response(response):
    pos = response.find(Constants.END_LINE)
    if pos != -1:
        return response[:pos]


def _parse_get_response(response):
    return response.split(Constants.END_LINE)


def _check_for_errors(result):
    if result == Errors.ERROR:
        log.error("Received error response")
        raise DriverUnknownException("Received error response")
    elif result == Errors.SERVER_ERROR:
        log.error("Received server error")
        raise DriverServerException("Received server error")
    elif result == Errors.CLIENT_ERROR:
        log.error("Received client error")
        raise DriverClientException("Received client error")
