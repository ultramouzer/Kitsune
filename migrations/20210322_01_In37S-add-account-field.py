"""
Add account field
"""

from yoyo import step

__depends__ = {'20210321_01_m7Fuq-add-account-tables'}

steps = [
    step(
        """
        ALTER TABLE account
        ADD COLUMN created_at timestamp without time zone not null default CURRENT_TIMESTAMP
        """
    )
]
