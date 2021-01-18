from flask import Flask, request
from indexer import index_artists
from yoyo import read_migrations
from yoyo import get_backend
import patreon_importer
import fanbox_importer
import subscribestar_importer
import threading
import config
import uuid
app = Flask(__name__)

@app.before_first_request
def start():
    backend = get_backend(f'postgres://{config.database_user}:{config.database_password}@{config.database_host}/{config.database_dbname}')
    migrations = read_migrations('./migrations')
    with backend.lock():
        backend.apply_migrations(backend.to_apply(migrations))
    
    index_artists()

@app.route('/api/import', methods=['POST'])
def import_api():
    log_id = str(uuid.uuid4())
    if not request.args.get('session_key'):
        return "", 401
    if request.args.get('service') == 'patreon':
        th = threading.Thread(target=patreon_importer.import_posts, args=(log_id, request.args.get('session_key')))
        th.start()
    elif request.args.get('service') == 'fanbox':
        th = threading.Thread(target=fanbox_importer.import_posts, args=(log_id, request.args.get('session_key')))
        th.start()
    elif request.args.get('service') == 'subscribestar':
        th = threading.Thread(target=subscribestar_importer.import_posts, args=(log_id, request.args.get('session_key')))
        th.start()
    return log_id, 200