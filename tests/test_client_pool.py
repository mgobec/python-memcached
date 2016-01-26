from unittest import TestCase
from driver.client_pool import ClientPool
from driver.exceptions import  *


_TEST_KEY = 'testkey'
_TEST_VALUE = 'testvalue'
_EMPTY_VALUE = 'emptyvalue'
_server = ('localhost', 11211)


class MockClient(object):
    def __init__(self):
        self.connected = False
        self.data = {}

    def connect(self):
        self.connected = True

    def disconnect(self):
        self.connected = False

    def get(self, key):
        if key not in self.data:
            return _EMPTY_VALUE
        return self.data[key]

    def set(self, key, value, expire=0, noreply=True):
        if key in self.data:
            return False
        self.data[key] = value
        return True


class ClientPoolSingleClientTests(TestCase):
    def setUp(self):
        self.client = MockClient()
        self.client_pool = ClientPool(_server, 1)
        self.client_pool._free_clients.append(self.client)

    def test_set_value(self):
        result = self.client_pool.set(_TEST_KEY, _TEST_VALUE)
        self.assertTrue(result)
        self.assertEqual(_TEST_VALUE, self.client.data[_TEST_KEY])

    def test_get_value(self):
        self.client.data[_TEST_KEY] = _TEST_VALUE
        result = self.client_pool.get(_TEST_KEY)
        self.assertEqual(_TEST_VALUE, result)

    def test_get_no_value(self):
        result = self.client_pool.get(_TEST_KEY)
        self.assertEqual(_EMPTY_VALUE, result)

    def test_set_exists(self):
        result = self.client_pool.set(_TEST_KEY, _TEST_VALUE)
        self.assertTrue(result)
        result = self.client_pool.set(_TEST_KEY, _TEST_VALUE)
        self.assertFalse(result)

    def test_can_execute(self):
        self.assertTrue(self.client_pool.can_execute())
        self.client_pool._free_clients.clear()
        self.client_pool._used_clients.append(self.client)
        self.assertFalse(self.client_pool.can_execute())

    def test_max_clients_reached(self):
        with self.client_pool._client() as client1:
            with self.assertRaises(DriverConnectionLimitExceededException):
                self.assertFalse(self.client_pool.can_execute())
                with self.client_pool._client() as client2:
                    self.assertTrue(False)

    def test_max_clients_reached_unlocked(self):
        self.client_pool._free_clients.clear()
        self.client_pool._used_clients.append(self.client)
        with self.assertRaises(DriverConnectionLimitExceededException):
            with self.client_pool._client() as client:
                self.assertTrue(False)

    def test_can_execute_with_lock(self):
        self.assertTrue(self.client_pool.can_execute())
        with self.client_pool._client() as client:
            self.assertFalse(self.client_pool.can_execute())
            self.assertEqual(0, len(self.client_pool._free_clients))
            self.assertEqual(1, len(self.client_pool._used_clients))

    def test_dispose(self):
        self.client_pool.dispose()
        self.assertFalse(self.client.connected)
        self.assertEqual(0, len(self.client_pool._free_clients))


class ClientPoolMultipleClientTest(TestCase):
    def setUp(self):
        self.count = 10
        self.client_pool = ClientPool(_server, self.count)
        self.client_mocks = []
        for i in range(0, self.count):
            mock = MockClient()
            self.client_mocks.append(mock)
            self.client_pool._free_clients.append(mock)

    def test_multiple_set(self):
        self._recursive_loop_set_value(self.client_pool)
        for mock in self.client_mocks:
            self.assertEqual(_TEST_VALUE, mock.data[_TEST_KEY])

    def _recursive_loop_set_value(self, client_pool):
        with client_pool._client() as client:
            result = client.set(_TEST_KEY, _TEST_VALUE)
            self.assertTrue(result)
            if client_pool.can_execute():
                self._recursive_loop_set_value(client_pool)

    def test_multiple_get(self):
        for mock in self.client_mocks:
            mock.data[_TEST_KEY] = _TEST_VALUE
        self._recursive_loop_get_value(self.client_pool)

    def _recursive_loop_get_value(self, client_pool):
        with client_pool._client() as client:
            result = client.get(_TEST_KEY)
            self.assertEqual(result, _TEST_VALUE)
            if client_pool.can_execute():
                self._recursive_loop_get_value(client_pool)

    def test_max_clients_can_execute(self):
        self._recursive_loop_without_exception(self.client_pool)

    def _recursive_loop_without_exception(self, client_pool):
        with client_pool._client() as client:
            if client_pool.can_execute():
                self._recursive_loop_without_exception(client_pool)

    def test_max_clients_reached(self):
        with self.assertRaises(DriverConnectionLimitExceededException):
            self._recursive_loop_with_exception(self.client_pool, self.count, 0)

    def _recursive_loop_with_exception(self, client_pool, count, current):
        with client_pool._client() as client:
            current += 1
            if count == current:
                self.assertFalse(client_pool.can_execute())
            self._recursive_loop_with_exception(client_pool, count, current)
