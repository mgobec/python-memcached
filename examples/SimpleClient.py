import sys
import logging

from driver.client import Client

logging.basicConfig(stream=sys.stdout,
                    level=logging.DEBUG,
                    format='[%(asctime)s] [%(levelname)s] %(name)-12s: %(message)s')


# Simple client example
def main():
    # Create client instance and connect to memcached
    server = ('localhost', 11211)
    client = Client(server)
    client.connect()

    # Set value
    result = client.set('testkey', 'testvalue')
    print(result)

    # Get value
    result = client.get('testkey')
    print(result)

if __name__ == "__main__":
    sys.exit(main())