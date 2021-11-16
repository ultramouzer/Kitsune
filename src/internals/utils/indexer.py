from src.lib.artist import index_artists
from setproctitle import setthreadtitle
import time

def run():
    setthreadtitle('KINDEXER')
    while True:
        index_artists()
        time.sleep(300)