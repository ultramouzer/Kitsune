import os
from .env_vars import (
    flask_env, 
    proxies,
    database_host,
    database_dbname,
    database_user,
    database_password,
    download_path
)

is_production = flask_env == 'production'
proxy_list = proxies.split(',')
database_url = f"postgres://{database_user}:{database_password}@{database_host}/{database_dbname}"
icons_path = os.path.join(download_path, 'icons')
banners_path = os.path.join(download_path, 'banners')
