"""
Add DM indexes
"""

from yoyo import step

__depends__ = {'20210707_03_m9nL9-add-temp-dm-tables'}

steps = [
    step('CREATE INDEX unapproved_dm_idx ON unapproved_dms USING btree ("import_id")', 'DROP INDEX unapproved_dm_idx'),
    step('CREATE INDEX dm_idx ON dms USING btree ("user")', 'DROP INDEX dm_idx')
]
