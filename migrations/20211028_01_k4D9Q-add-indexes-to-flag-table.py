"""
Add indexes to flag table
"""

from yoyo import step

__depends__ = {'20211014_02_J099n-add-indexes-to-new-saved-key-table'}

steps = [
    step('CREATE INDEX flag_id_idx ON booru_flags USING btree ("id")', 'DROP INDEX flag_id_idx'),
    step('CREATE INDEX flag_user_idx ON booru_flags USING btree ("user")', 'DROP INDEX flag_user_idx'),
    step('CREATE INDEX flag_service_idx ON booru_flags USING btree ("service")', 'DROP INDEX flag_service_idx')
]
