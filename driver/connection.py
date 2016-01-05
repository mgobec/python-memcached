import socket
import logging

import six


_DEAD_RETRY = 30  # number of seconds before retrying a dead server.
_SOCKET_TIMEOUT = 3  # number of seconds before sockets timeout.

log = logging.getLogger(__name__)


class Connection(object):

    def __init__(self,
                 host_ip='localhost',
                 host_port=11211,
                 dead_retry=_DEAD_RETRY,
                 socket_timeout=_SOCKET_TIMEOUT):
        self.host_ip = host_ip
        self.host_port = host_port
        self.dead_retry = dead_retry
        self.socket_timeout = socket_timeout

        self.address = (self.host_ip, self.host_port)
        self.socket = None
        self.buffer = b''

    def connect(self):
        if self._open_socket():
            return 1
        return 0

    def disconnect(self):
        if self.socket:
            self.socket.close()
            self.socket = None

    def send_cmd(self, command):
        if isinstance(command, six.text_type):
            command = command.encode('utf8')
        self.socket.sendall(command + b'\r\n')

    def _open_socket(self):
        if self.socket:
            return self.socket

        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        if hasattr(s, 'settimeout'):
            s.settimeout(self.socket_timeout)

        try:
            s.connect(self.address)
        except socket.timeout as msg:
            log.error("Timeout while connecting to %s with message: %s" %
                      (self.address, msg))
            return None
        except socket.error as msg:
            if isinstance(msg, tuple):
                msg = msg[1]
            log.error("Error while connecting to %s with message: %s" %
                      (self.address, msg))
            return None

        self.socket = s
        self.buffer = b''

        return s

