from ..internals.utils.logger import log

def import_posts(import_id, target, args):
    try:
        target(import_id, *args)
    except:
        log(import_id, 'Internal error. Contact site staff on Telegram.', 'exception')
