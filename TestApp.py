import driver

import logging
import sys

logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)


def main():
    server = ('localhost', 11211)
    # connection = driver.Connection(server)
    # connection.open()
    # connection.close()
    client = driver.Client(server)
    result = client.set("testkey", "testvalue")
    print(result)
    print("Success")
    return 0

if __name__ == "__main__":
    sys.exit(main())
