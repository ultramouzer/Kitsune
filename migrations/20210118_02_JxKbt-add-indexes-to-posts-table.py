"""
Add indexes to posts table
"""

from yoyo import step

__depends__ = {'20210118_01_1Jlkq-add-unique-constraint-to-service-and-post-fields'}

steps = [
    step('CREATE INDEX id_idx ON posts USING hash ("id")', 'DROP INDEX id_idx'),
    step('CREATE INDEX service_idx ON posts USING btree ("service")', 'DROP INDEX service_idx'),
    step('CREATE INDEX added_idx ON posts USING btree ("added")', 'DROP INDEX added_idx'),
    step('CREATE INDEX published_idx ON posts USING btree ("published")', 'DROP INDEX published_idx'),
    step('CREATE INDEX user_idx ON posts USING btree ("user")', 'DROP INDEX user_idx'),
    step('CREATE INDEX updated_idx ON posts USING btree ("user", "service", "added")', 'DROP INDEX updated_idx'),
]
