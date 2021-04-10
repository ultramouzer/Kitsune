from flask import Blueprint, request
import json

from ..internals.utils.utils import get_import_id
from ..internals.utils import logger
from ..internals.utils.flask_thread import FlaskThread

from ..importers import patreon
from ..importers import fanbox
from ..importers import subscribestar
from ..importers import gumroad

api = Blueprint('api', __name__)

@api.route('/api/import', methods=['POST'])
def import_api():
    key = request.args.get('session_key')
    import_id = get_import_id(key)

    print('got hit to import', import_id)

    if not key:
        return "", 401
    if request.args.get('service') == 'patreon':
        print('requesting service patreon')
        th = FlaskThread(target=patreon.import_posts, args=(import_id, key)).start()
    elif request.args.get('service') == 'fanbox':
        th = FlaskThread(target=fanbox.import_posts, args=(import_id, key)).start()
    elif request.args.get('service') == 'subscribestar':
        th = FlaskThread(target=subscribestar.import_posts, args=(import_id, key)).start()
    elif request.args.get('service') == 'gumroad':
        th = FlaskThread(target=gumroad.import_posts, args=(import_id, key)).start()
    return import_id, 200

@api.route('/api/logs/<log_id>', methods=['GET'])
def get_logs(log_id):
    logs = logger.get_logs(log_id)
    return json.dumps(logs), 200
