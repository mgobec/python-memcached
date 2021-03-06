import socket
import logging


_DEAD_RETRY = 30  # number of seconds before retrying a dead server.
_SOCKET_TIMEOUT = 3  # number of seconds before sockets timeout.
_RECEIVE_SIZE = 4096

log = logging.getLogger(__name__)


class Connection(object):
    """
    Socket connection wrapper handling low level connection logic
    """

    def __init__(self,
                 server=('localhost', 11211),
                 dead_retry=_DEAD_RETRY,
                 socket_timeout=_SOCKET_TIMEOUT):
        self.dead_retry = dead_retry
        self.socket_timeout = socket_timeout

        self.server = server
        self.socket = None

    def open(self):
        """
        Open the socket
        :return: Returns true if success
        """
        if self._open_socket():
            log.debug("Connection open")
            return True
        return False

    def close(self):
        """
        Close the socket
        """
        if self.socket:
            self.socket.close()
            log.debug("Connection closed")
            self.socket = None

    def send(self, data):
        """
        Send data over the socket
        :param data: Data to be sent
        """
        log.debug("Sending data: %s" % data)
        self.socket.sendall(data)

    def _open_socket(self):
        if self.socket:
            return self.socket

        new = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        if hasattr(new, 'settimeout'):
            new.settimeout(self.socket_timeout)

        try:
            new.connect(self.server)
            log.debug("Socket connected")

        except socket.timeout as msg:
            log.error("Timeout while connecting to %s with message: %s" %
                      (self.server, msg))
            return None
        except socket.error as msg:
            if isinstance(msg, tuple):
                msg = msg[1]
            log.error("Error while connecting to %s with message: %s" %
                      (self.server, msg))
            return None

        self.socket = new

        return new

    def read(self, size=_RECEIVE_SIZE):
        """
        Receive data from socket
        :param size: Size of data to receive
        :return: Received data
        """
        try:
            return self.socket.recv(size)
        except IOError as ex:
            log.error("Error while reading from socket", ex)
            raise
