from os import getenv

flask_env = getenv('FLASK_ENV', 'development')
download_path = getenv('DOWNLOAD_PATH', '/storage')

# database info
database_host = getenv('DATABASE_HOST', 'localhost')
database_dbname = getenv('DATABASE_DBNAME', 'kemonodb')
database_user = getenv('DATABASE_USER', 'nano')
database_password = getenv('DATABASE_PASSWORD', 'shinonome')

redis_host = getenv('REDIS_HOST', 'localhost')
redis_port = getenv('REDIS_PORT', '6379')

# proxies = ["socks5://user:pass@host:port"]
proxies = getenv('PROXIES', '')

ban_url = getenv('BAN_URL', '')
