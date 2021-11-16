# from pathlib import Path

from configs.constants import dev_path
from development.utils import get_folder_file_paths

file_extensions = ['gif', 'jpeg', 'jpg', 'png', 'webp']
assets_folder = dev_path.joinpath('assets')
asset_files = get_folder_file_paths(assets_folder, file_extensions)
