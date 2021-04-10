from flask import Blueprint, request
from ..internals.utils.utils import get_import_id
from ..internals.utils.logger import get_logs

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
    if request.args.get('service') == 'patreon':
        th = threading.Thread(target=patreon.import_posts, args=(import_id, key))
        th.start()
    elif request.args.get('service') == 'fanbox':
        th = threading.Thread(target=fanbox.import_posts, args=(import_id, key))
        th.start()
    elif request.args.get('service') == 'subscribestar':
        th = threading.Thread(target=subscribestar.import_posts, args=(import_id, key))
        th.start()
    elif request.args.get('service') == 'gumroad':
        th = threading.Thread(target=gumroad.import_posts, args=(import_id, key))
        th.start()
    return import_id, 200

@api.route('/api/logs', methods=['GET'])
def get_logs():
    logs = get_logs()
    if len(logs) > 0:
        return json.dumps(logs), 200
    else:
        return "", 204
