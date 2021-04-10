from flask import current_app, session

from threading import Lock
from .utils import get_value

log_lock = Lock()

def log(msg, level = 'debug', to_client = False):
    log_lock.acquire()
    try:
        log_func = getattr(current_app.logger, level)
        log_func(msg)

        if 'logs' not in session:
            session['logs'] = []
        if to_client:
            session['logs'].append(msg)
    finally:
        log_lock.release()

def get_logs():
    log_lock.acquire()
    try:
        messages = get_value(session, 'logs')
        session['logs'] = []
        return messages
    finally:
        log_lock.release()
