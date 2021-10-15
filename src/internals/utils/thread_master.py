from typing import List
from threading import Thread
# a function that starts other threads in a staggered manner
# needs to be run in a thread itself
def run(threads: List[Thread], limit=10):
    offset = 0
    while True:
        threads_to_run = threads[offset:offset+limit]
        if (len(threads_to_run) == 0):
            break
        for thread in threads_to_run:
            thread.start()
        for thread in threads_to_run:
            thread.join()
        offset += limit