"""
Create auto-import tables
"""

from yoyo import step

__depends__ = {'20210926_01_5n9U4-create-file-tracking-tables'}

steps = [
    step(
        """
        CREATE TABLE saved_session_keys (
            id serial primary key,
            service varchar not null,
            discord_channel_ids varchar,
            encrypted_key varchar not null,
            added timestamp not null DEFAULT CURRENT_TIMESTAMP,
            dead boolean not null DEFAULT FALSE,
            contributor_id int REFERENCES account(id),
            UNIQUE (service, encrypted_key)
        );
        """,
        "DROP TABLE saved_session_keys"
    ),
    step(
        """
        CREATE TABLE saved_session_key_import_ids (
            key_id int not null REFERENCES saved_session_keys(id),
            import_id varchar not null,
            UNIQUE (key_id, import_id)
        );
        """,
        "DROP TABLE saved_session_key_import_ids"
    ),
    step('CREATE INDEX saved_session_keys_contributor_idx ON saved_session_keys USING btree ("contributor_id")', 'DROP INDEX saved_session_keys_contributor_idx'),
    step('CREATE INDEX saved_session_keys_dead_idx ON saved_session_keys USING btree ("dead")', 'DROP INDEX saved_session_keys_contributor_idx')
]
