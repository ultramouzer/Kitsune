"""
Variables which derive off environment variables go there.
"""
from pathlib import Path

from .vars import flask_env, download_path

is_development = flask_env == 'development'
temp_dir_root = Path(download_path, 'data', 'tmp')
data_folder = Path(download_path, 'data')
