"""
Environment variable assignments are stored there.
No transformation allowed, therefore all variables there are strings.
"""

import os

flask_env = os.getenv('FLASK_ENV', 'development')
