"""
Add sha256hash column to saved key table
"""

from yoyo import step

__depends__ = {'20210927_01_administrator-groundwork'}

steps = [
    step(
        """
        CREATE TABLE saved_session_keys_with_hashes (
            id serial primary key,
            service varchar not null,
            discord_channel_ids varchar,
            encrypted_key varchar not null,
            hash varchar not null,
            added timestamp not null DEFAULT CURRENT_TIMESTAMP,
            dead boolean not null DEFAULT FALSE,
            contributor_id int REFERENCES account(id),
            UNIQUE (service, hash)
        );
        """,
        "DROP TABLE saved_session_keys_with_hashes"
    ),
    step(
        "ALTER TABLE saved_session_key_import_ids DROP CONSTRAINT saved_session_key_import_ids_key_id_fkey;",
        "ALTER TABLE saved_session_key_import_ids ADD CONSTRAINT saved_session_key_import_ids_key_id_fkey FOREIGN KEY (key_id) REFERENCES saved_session_keys(id);"
    )
    # will add another constraint later for the new table in a separate commit, otherwise it'll complain that things are missing
    # step(
    #     "ALTER TABLE saved_session_key_import_ids ADD CONSTRAINT saved_session_key_import_ids_key_id_fkey FOREIGN KEY (key_id) REFERENCES saved_session_keys(id);",
    #     "ALTER TABLE saved_session_key_import_ids DROP CONSTRAINT saved_session_key_import_ids_key_id_fkey;"
    # ),
]
