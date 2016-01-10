import driver

import logging
import sys

logging.basicConfig(stream=sys.stdout,
                    level=logging.DEBUG,
                    format='[%(asctime)s] [%(levelname)s] %(name)-12s: %(message)s')


def main():
    server = ('localhost', 11211)
    # connection = driver.Connection(server)
    # connection.open()
    # connection.close()
    client = driver.Client(server)
    result = client.set("testkey1", "testvalue1")
    print(result)
    result = client.set("testkey2", "testvalue2")
    print(result)
    result = client.get("testkey1")
    print(result)
    result = client.get("testkey2")
    print(result)

    # for i in range(0, 1000):
    #     print(client.get("testkey"))

    return 0

if __name__ == "__main__":
    sys.exit(main())
