from flask import Flask, g
from yoyo import read_migrations
from yoyo import get_backend
import logging
import uwsgi
import config

from configs.derived_vars import is_development
from src.endpoints.api import api
from src.endpoints.icons import icons
from src.endpoints.banners import banners
from src.internals.database import database
from src.internals.cache import redis

from src.lib.artist import index_artists
from src.internals.database.database import get_raw_conn

app = Flask(__name__)

app.register_blueprint(api)
app.register_blueprint(icons)
app.register_blueprint(banners)
if is_development:
    from development import development
    app.register_blueprint(development)

logging.basicConfig(filename='kemono_importer.log', level=logging.DEBUG)
logging.getLogger('requests').setLevel(logging.WARNING)
logging.getLogger('urllib3').setLevel(logging.WARNING)

database.init()
redis.init()

if uwsgi.worker_id() == 0:
    backend = get_backend(f'postgres://{config.database_user}:{config.database_password}@{config.database_host}/{config.database_dbname}')
    migrations = read_migrations('./migrations')
    with backend.lock():
        backend.apply_migrations(backend.to_apply(migrations))
    index_artists()

@app.teardown_appcontext
def close(e):
    cursor = g.pop('cursor', None)
    if cursor is not None:
        cursor.close()
        connection = g.pop('connection', None)
        if connection is not None:
            try:
                connection.commit()
                pool = database.get_pool()
                pool.putconn(connection)
            except:
                pass
