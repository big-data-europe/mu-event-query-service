import os
import queries
import json
import signal
import sys
from time import time, sleep

timenow = time()

def signal_handler(signal, frame):
    """
    Remove the containers information file if it exists upon recieving either SIGINT or SIGKILL.
    """
    try:
        os.remove(os.environ['WRITE_DIR'] + os.environ['WRITE_FILE'])
    except OSError:
        pass
    sys.exit(0)

def main_loop():
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)

    while True:
        containers = queries.list_container_events(timenow)
        queries.write_json_into_file(containers)

        sleep(int(os.environ['SLEEP_PERIOD']))

main_loop()
