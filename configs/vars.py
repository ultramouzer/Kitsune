"""
Environment variable assignments are stored there.
No transformation allowed, therefore all variables there are strings.

TODO: deal with `config.py` file
"""

import os
import config

flask_env = os.getenv('FLASK_ENV', 'development')
download_path = config.download_path or '/storage'
