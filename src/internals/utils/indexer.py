from src.lib.artist import index_artists
import time

def run():
    while True:
        index_artists()
        time.sleep(300)