import six
import logging

from driver.connection import Connection
from driver.exceptions import *
from driver.protocol import *


log = logging.getLogger(__name__)


class Client(object):
    """ Memcached client implementation with simple get and set methods

    Args:
        server: Connection parameters

    Provides socket and protocol implementation for get and set commands.
    To leverage parallel execution use ClientPool class.
    """
    def __init__(self, server):
        self._server = server
        self._connection = Connection(server)

    def connect(self):
        """
        Open socket connection to memcached instance
        """
        return self._connection.open()

    def disconnect(self):
        """
        Close socket connection to memcached instance
        """
        self._connection.close()

    def get(self, key):
        """
        Executes get command
        :param key: Key of the value to get
        :return: Value for given key
        """
        if not self._connection.socket:
            self._connection.open()

        command = b'get' +\
                  b' ' + _encode(key) +\
                  Constants.END_LINE

        try:
            self._connection.send(command)
        except Exception as ex:
            log.error("Command failed: %s" % str(command), ex)
            self._connection.close()
            return None

        try:
            response = self._connection.read()
        except Exception as ex:
            log.error("Failed to read response from socket", ex)
            self._connection.close()
            return None

        log.debug("Received from socket: %s" % response)
        result = _parse_get_response(response)
        _check_for_errors(result[0])
        if len(result) > 2:
            return result[1]

        raise DriverUnknownException(
            "Received unexpected response from the memcached instance %s" % str(result))

    def set(self, key, value, expire=0, noreply=True):
        """
        Executes set command
        :param key: Key of the value to set
        :param value: String value
        :param expire: Expire time with default value of never (0)
        :param noreply: Indicates if client should wait for response
        :return: Returns indication of a successful write
        Set method execution time can benefit from skipping wait for reply
        """
        if not self._connection.socket:
            self._connection.open()

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

        if expire > Constants.MAXIMUM_TTL:
            log.info("Using a value of TTL larger than max ttl. \
            The value provided will be converted into unix timestamp for ttl timeout")

        command = b'set' +\
                  b' ' + _encode(key) +\
                  b' ' + _encode(flags) +\
                  b' ' + _encode(expire) +\
                  b' ' + _encode(len(value)) +\
                  arguments + Constants.END_LINE +\
                  value + Constants.END_LINE

        try:
            self._connection.send(command)
        except Exception as ex:
            log.error("Command failed: %s" % str(command), ex)
            self._connection.close()
            return False

        if noreply:
            return True

        try:
            response = self._connection.read()
        except Exception as ex:
            log.error("Failed to read response from socket", ex)
            self._connection.close()
            return False

        result = response.rstrip(Constants.END_LINE).split(Constants.END_LINE)
        log.debug("Received from socket: %s" % response)

        if result[0] == StoreReply.STORED:
            log.debug("Successfully stored data")
            return True
        elif result[0] == StoreReply.EXISTS:
            log.debug("Entry already exists")
            return False
        elif result[0] == StoreReply.NOT_STORED:
            log.warn("Entry not stored for some reason")
            return False
        elif result[0] == StoreReply.NOT_FOUND:
            log.warn("Received not found response")
            return False

        _check_for_errors(result[0])

        raise DriverUnknownException(
            "Received unexpected response from the memcached instance %s" % str(response))


def _encode(data):
    return six.text_type(data).encode('ascii')


def _parse_get_response(response):
    return response.split(Constants.END_LINE)


def _check_for_errors(result):
    if result == Errors.ERROR:
        message = "Received error response"
        log.error(message)
        raise DriverUnknownException(message)
    elif result.startswith(Errors.SERVER_ERROR):
        message = "Received server error with message: %s" % result[result.find(b' ') + 1:].decode("utf-8")
        log.error(message)
        raise DriverServerException(message)
    elif result.startswith(Errors.CLIENT_ERROR):
        message = "Received client error with message: %s" % result[result.find(b' ') + 1:].decode("utf-8")
        log.error(message)
        raise DriverClientException(message)
