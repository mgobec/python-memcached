import logging
import collections
import threading
import six

from contextlib import contextmanager
from driver.exceptions import *
from driver.client import Client


log = logging.getLogger(__name__)


class ClientPool(object):
    """ Thread safe pool of clients creating up to max_clients for parallel execution

    Args:
        server: Connection parameters
        max_clients: Maximum number of clients to be created

    All clients are created only when needed so that the connection count is optimized
    for parallel usage but still lightweight on the resources.
    If a request is made when the maximum number of clients is reached exception will
    be thrown (DriverConnectionLimitExceededException). Client should track number of
    used clients in the pool by using can_execute method.
    """
    def __init__(self, server, max_clients):
        self.server = server
        if not isinstance(max_clients, six.integer_types) or max_clients <= 0:
            raise ValueError('"max_clients" parameter illegal value')
        self._max_clients = max_clients
        self._used_clients = collections.deque()
        self._free_clients = collections.deque()
        self._lock = threading.Lock()

    def can_execute(self):
        """
        Indicates if more commands can be executed in parallel
        :return: Returns boolean response
        """
        return len(self._used_clients) < self._max_clients

    def get(self, key):
        """
        Execute get command on first available client
        :param key: Key of the value to get
        :return: Value for given key
        """
        with self._client() as client:
            return client.get(key)

    def set(self, key, value, expire=0, noreply=True):
        """
        Execute set command on first available client
        :param key: Key of the value to set
        :param value: String value
        :param expire: Expire time with default value of never (0)
        :param noreply: Indicates if client should wait for response.
        :return: Returns response from memcached server
        Set method execution time can benefit from skipping wait for reply
        """
        with self._client() as client:
            return client.set(key, value, expire, noreply)

    def dispose(self):
        with self._lock:
            clients = []
            clients.extend(self._used_clients)
            clients.extend(self._free_clients)
            for client in clients:
                client.disconnect()
            self._used_clients.clear()
            self._free_clients.clear()

    @contextmanager
    def _client(self):
        """
        Provides ability to use 'with' statement when executing commands so that
        the free client is handled in this method.
        """
        client = self._get_client()
        try:
            yield client
        except Exception as ex:
            log.error("Failed to get client from pool", ex)
            raise
        finally:
            self._free_client(client)

    def _get_client(self):
        with self._lock:
            if self._free_clients:
                # Get first free client from queue
                client = self._free_clients.pop()
                self._used_clients.append(client)
                return client

            # Check if max_clients limit has been reached
            if len(self._used_clients) >= self._max_clients:
                raise DriverConnectionLimitExceededException(
                        "Open clients limit reached. Cannot create more clients")

            # Create new client and use it
            log.debug("Creating new client")
            client = Client(self.server)
            if not client.connect():
                raise DriverConnectionException("Failed to connect to server")
            self._used_clients.append(client)
            return client

    def _free_client(self, client):
        with self._lock:
            try:
                self._used_clients.remove(client)
                self._free_clients.append(client)
            except Exception as ex:
                log.error("Failed to free client", ex)
