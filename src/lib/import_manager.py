from ..internals.utils.logger import log
from ..internals.cache.redis import delete_keys, delete_keys_pattern

def import_posts(import_id, target, args):
    try:
        target(import_id, *args)
    except KeyboardInterrupt:
        return
    except SystemExit:
        return
    except:
        log(import_id, 'Internal error. Contact site staff on Telegram.', 'exception')
    
    # cleanup on "internal" exit
    delete_keys([f'imports:{import_id}'])
    delete_keys_pattern([f'running_imports:*:{import_id}'])
