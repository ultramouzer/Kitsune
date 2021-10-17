from typing import List
from threading import Thread
# a function that starts other threads in a queue
# needs to be run in a thread itself
def run(threads: List[Thread], limit=10):
    pos = 0
    threads_to_run = []
    while pos < len(threads):
        for thread in threads_to_run:
            if not thread.is_alive():
                threads_to_run.remove(thread)
        if not len(threads_to_run) > limit:
            # start and add more threads until it reaches the slot limit
            while len(threads_to_run) < limit:
                thread = threads[pos]
                thread.start()
                threads_to_run.append(thread)
                pos += 1