"""
This folder holds development modules.
Only modules imported to this file are allowed to be imported outside.
These imports always have to be conditional, such as:
```python
if (is_development):
    from development import module_name
    module_name()
```
"""


from .lib import importer as kemono_dev
from .internals import service_name
from .blueprints import development
