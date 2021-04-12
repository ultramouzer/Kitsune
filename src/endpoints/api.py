from flask import Blueprint, request
import json

from ..internals.utils.flask_thread import FlaskThread
from ..internals.utils.utils import get_import_id
from ..internals.utils import logger
from ..lib.import_manager import import_posts

from ..importers import patreon
from ..importers import fanbox
from ..importers import subscribestar
from ..importers import gumroad

api = Blueprint('api', __name__)

@api.route('/api/import', methods=['POST'])
def import_api():
    key = request.args.get('session_key')
    import_id = get_import_id(key)

    if not key:
        return "", 401

    target = None
    args = None
    if request.args.get('service') == 'patreon':
        target = patreon.import_posts
        args = (key,)
    elif request.args.get('service') == 'fanbox':
        target = fanbox.import_posts
        args = (key,)
    elif request.args.get('service') == 'subscribestar':
        target = subscribestar.import_posts
        args = (key,)
    elif request.args.get('service') == 'gumroad':
        target = gumroad.import_posts
        args = (key,)

    if target is not None and args is not None:
        logger.log(import_id, f'Starting import. Your import id is {import_id}.')
        FlaskThread(target=import_posts, args=(import_id, target, args)).start()
    else:
        logger.log(import_id, f'Error starting import. Your import id is {import_id}.')

    return import_id, 200

@api.route('/api/logs/<log_id>', methods=['GET'])
def get_logs(log_id):
    logs = logger.get_logs(log_id)
    return json.dumps(logs), 200
