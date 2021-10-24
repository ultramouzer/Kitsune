import config
import redis
import random
import string
import time
import json
from .flask_thread import FlaskThread
from src.internals.utils import logger
from src.internals.utils.encryption import encrypt_and_log_session
from src.lib.import_manager import import_posts
from ..cache.redis import get_redis
from src.importers import patreon
from src.importers import fanbox
from src.importers import subscribestar
from src.importers import gumroad
from src.importers import discord
from src.importers import fantia

# a function that first runs existing import requests in a staggered manner (they may be incomplete as importers should delete their keys when they are done) then watches redis for new keys and handles queueing
# needs to be run in a thread itself
# remember to clear logs after successful import
def watch(queue_limit=50):
    archiver_id = ''.join(random.choice(string.ascii_letters + string.digits) for x in range(16))

    redis = get_redis()
    threads_to_run = []
    while True:
        for thread in threads_to_run:
            if not thread.is_alive():
                threads_to_run.remove(thread)
        
        keys = redis.keys('imports:*')
        for key in keys:
            key_data = redis.get(key)
            if key_data:
                key_data = json.loads(key_data)
                if redis.get(f"running_imports:{archiver_id}:{key_data['import_id']}"):
                    continue
                
                if len(threads_to_run) < queue_limit:
                    target = None
                    args = None
                    # data = {
                    #     'import_id': import_id,
                    #     'key': key,
                    #     'service': service,
                    #     'allowed_to_auto_import': allowed_to_auto_import,
                    #     'allowed_to_save_session': allowed_to_save_session,
                    #     'allowed_to_scrape_dms': allowed_to_scrape_dms,
                    #     'channel_ids': channel_ids,
                    #     'contributor_id': contributor_id
                    # }
                    import_id = key_data['import_id']
                    key = key_data['key']
                    service = key_data['service']
                    allowed_to_auto_import = key_data.get('auto_import', False)
                    allowed_to_save_session = key_data.get('save_session_key', False)
                    allowed_to_scrape_dms = key_data.get('save_dms', False)
                    channel_ids = key_data['channel_ids']
                    contributor_id = key_data['contributor_id']

                    if key and service and allowed_to_save_session:
                        try:
                            encrypt_and_log_session(import_id, service, key)
                        except:
                            pass
                    
                    if service == 'patreon':
                        target = patreon.import_posts
                        args = (key, allowed_to_scrape_dms, contributor_id, allowed_to_auto_import, None)
                    elif service == 'fanbox':
                        target = fanbox.import_posts
                        args = (key, contributor_id, allowed_to_auto_import, None)
                    elif service == 'subscribestar':
                        target = subscribestar.import_posts
                        args = (key, contributor_id, allowed_to_auto_import, None)
                    elif service == 'gumroad':
                        target = gumroad.import_posts
                        args = (key, contributor_id, allowed_to_auto_import, None)
                    elif service == 'fantia':
                        target = fantia.import_posts
                        args = (key, contributor_id, allowed_to_auto_import, None)
                    elif service == 'discord':
                        target = discord.import_posts
                        args = (key, channel_ids.strip().replace(" ", ""), contributor_id, allowed_to_auto_import, None)

                    if target is not None and args is not None:
                        logger.log(import_id, f'Starting import. Your import id is {import_id}.')
                        thread = FlaskThread(target=import_posts, args=(import_id, target, args))
                        thread.start()
                        threads_to_run.append(thread)
                        redis.set(f"running_imports:{archiver_id}:{key_data['import_id']}", '1')
                    else:
                        logger.log(import_id, f'Error starting import. Your import id is {import_id}.')
        
        time.sleep(1)