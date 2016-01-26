import collections
import unittest
import driver
from driver.protocol import *

_server = ('localhost', 11211)
_dead_retry = 30
_socket_timeout = 3
_max_receive_size = 4096


class MockConnection(object):
    def __init__(self,
                 server=_server,
                 dead_retry=30,
                 socket_timeout=3):
        self.server = server
        self.dead_retry = dead_retry
        self.socket_timeout = socket_timeout
        self.closed = True
        self.socket = None
        self.send_buffer = collections.deque()
        self.receive_buffer = collections.deque()
        self.on_read = None
        self.on_write = None

    def open(self):
        self.closed = False
        self.socket = True
        return True

    def close(self):
        self.closed = True
        self.socket = None

    def send(self, data):
        if self.on_write is not None:
            self.on_write()
        self.send_buffer.append(data)

    def read(self, size=_max_receive_size):
        if self.on_read is not None:
            self.on_read()
        return self.receive_buffer.popleft()


class ClientTests(unittest.TestCase):
    def setUp(self):
        self.client = driver.Client(_server)
        self.mock = MockConnection()
        self.client._connection = self.mock
        self.client.connect()

    def test_initialize_and_connect(self):
        self.assertFalse(self.mock.closed)

    def test_disconnect(self):
        self.client.disconnect()
        self.assertTrue(self.mock.closed)

    def test_set_value_without_response(self):
        self.client.set('testkey', 'testvalue')
        self.assertEqual(self.mock.send_buffer.pop(), b'set testkey 0 0 9 noreply\r\ntestvalue\r\n')

    def test_set_value_with_stored_response(self):
        self.mock.receive_buffer.append(StoreReply.STORED + Constants.END_LINE)
        response = self.client.set('testkey', 'testvalue', 0, False)
        self.assertTrue(response)

    def test_set_value_with_not_stored_response(self):
        self.mock.receive_buffer.append(StoreReply.NOT_STORED + Constants.END_LINE)
        response = self.client.set('testkey', 'testvalue', 0, False)
        self.assertFalse(response)

    def test_set_value_with_exists_response(self):
        self.mock.receive_buffer.append(StoreReply.EXISTS + Constants.END_LINE)
        response = self.client.set('testkey', 'testvalue', 0, False)
        self.assertFalse(response)

    def test_set_value_with_error_response(self):
        self.mock.receive_buffer.append(Errors.ERROR + Constants.END_LINE)
        with self.assertRaises(driver.DriverUnknownException):
            self.client.set('testkey', 'testvalue', 0, False)

    def test_set_value_with_server_error_response(self):
        self.mock.receive_buffer.append(Errors.SERVER_ERROR + b' Test server error' + Constants.END_LINE)
        with self.assertRaises(driver.DriverServerException):
            self.client.set('testkey', 'testvalue', 0, False)

    def test_set_value_with_client_error_response(self):
        self.mock.receive_buffer.append(Errors.CLIENT_ERROR + b' Test client error' + Constants.END_LINE)
        with self.assertRaises(driver.DriverClientException):
            self.client.set('testkey', 'testvalue', 0, False)

    def test_set_value_exception(self):
        error_message = "Test write exception"
        self.mock.on_write = lambda: _raise_exception(error_message)
        result = self.client.set('testkey', 'testvalue', 0, False)
        self.assertFalse(result)

    def test_get_value_exception(self):
        error_message = "Test read exception"
        self.mock.on_read = lambda: _raise_exception(error_message)
        result = self.client.get('testkey')
        self.assertIsNone(result)


def _raise_exception(message):
    raise Exception(message)
