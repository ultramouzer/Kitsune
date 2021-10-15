"""
Add indexes to new saved key table
"""

from yoyo import step

__depends__ = {'20211014_01_1hR6J-add-sha256hash-column-to-saved-key-table'}

steps = [
    step('CREATE INDEX saved_session_keys_with_hashes_contributor_idx ON saved_session_keys_with_hashes USING btree ("contributor_id")', 'DROP INDEX saved_session_keys_with_hashes_contributor_idx'),
    step('CREATE INDEX saved_session_keys_with_hashes_dead_idx ON saved_session_keys_with_hashes USING btree ("dead")', 'DROP INDEX saved_session_keys_with_hashes_dead_idx')
]
