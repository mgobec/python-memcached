import driver

import logging
import sys
import threading

logging.basicConfig(stream=sys.stdout,
                    level=logging.DEBUG,
                    format='[%(asctime)s] [%(levelname)s] %(name)-12s: %(message)s')


# Define concurrent task
def task(pool, key):
    for i in range(0, 10):
        result = pool.get(key)
        print(result)


def main():
    # Define max clients and initialize client pool
    max_connections = 10
    server = ('localhost', 11211)
    client_pool = driver.ClientPool(server, max_connections)

    # Create some tasks that will read in parallel
    tasks = []
    for i in range(0, 10):
        val = str(i + 1)
        # Insert some test data to be read
        result = client_pool.set('testkey' + val, 'testvalue' + val, 0, False)
        print(result)

        # Read data inserted
        result = client_pool.get('testkey' + val)
        print(result)

        # Create task with reading method loop
        tasks.append(threading.Thread(target=task, args=(client_pool, 'testkey' + val,)))

    for t in tasks:
        t.start()

    for t in tasks:
        t.join()

    # Dispose client pool
    client_pool.dispose()

if __name__ == "__main__":
    sys.exit(main())
