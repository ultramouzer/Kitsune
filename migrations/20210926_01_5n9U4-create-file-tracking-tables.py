"""
Create file tracking tables
"""

from yoyo import step

__depends__ = {'20210805_01_riCyY-index-dms-for-search'}

steps = [
    step(
        """
        CREATE TABLE files (
            id serial primary key,
            hash varchar not null,
            mtime timestamp not null,
            ctime timestamp not null,
            mime varchar,
            ext varchar,
            added timestamp not null DEFAULT CURRENT_TIMESTAMP,
            UNIQUE(hash)
        );
        """,
        "DROP TABLE files;"
    ),
    step(
        """
        CREATE TABLE file_post_relationships (
            file_id int not null REFERENCES files(id),
            filename varchar not null,
            service varchar not null,
            user varchar not null,
            post varchar not null,
            contributor_id varchar REFERENCES account(id),
            inline boolean not null DEFAULT FALSE,
            PRIMARY KEY (file_id, service, user, post)
        );
        """,
        "DROP TABLE file_post_relationships;"
    ),
    step(
        """
        CREATE TABLE file_discord_message_relationships (
            file_id int not null REFERENCES files(id),
            filename varchar not null,
            server varchar not null,
            channel varchar not null,
            id varchar not null,
            contributor_id varchar REFERENCES account(id),
            PRIMARY KEY (file_id, server, channel, id)
        );
        """,
        "DROP TABLE file_discord_message_relationships;"
    ),
    step(
        """
        CREATE TABLE file_server_relationships (
            file_id int not null REFERENCES files(id),
            remote_path varchar not null
        );
        """,
        "DROP TABLE file_server_relationships;"
    ),
    step('CREATE INDEX file_id_idx ON file_post_relationships USING btree ("file_id")', 'DROP INDEX file_id_idx'),
    step('CREATE INDEX file_post_service_idx ON file_post_relationships USING btree ("service")', 'DROP INDEX file_post_service_idx'),
    step('CREATE INDEX file_post_user_idx ON file_post_relationships USING btree ("user")', 'DROP INDEX file_post_user_idx'),
    step('CREATE INDEX file_post_id_idx ON file_post_relationships USING btree ("id")', 'DROP INDEX file_post_id_idx'),
    step('CREATE INDEX file_post_contributor_id_idx ON file_post_relationships USING btree ("contributor_id")', 'DROP INDEX file_post_contributor_id_idx'),
    step('CREATE INDEX file_discord_id_idx ON file_discord_message_relationships USING btree ("file_id")', 'DROP INDEX file_discord_id_idx'),
    step('CREATE INDEX file_discord_message_server_idx ON file_discord_message_relationships USING btree ("server")', 'DROP INDEX file_discord_message_server_idx'),
    step('CREATE INDEX file_discord_message_channel_idx ON file_discord_message_relationships USING btree ("channel")', 'DROP INDEX file_discord_message_channel_idx'),
    step('CREATE INDEX file_discord_message_id_idx ON file_discord_message_relationships USING btree ("id")', 'DROP INDEX file_discord_message_id_idx'),
    step('CREATE INDEX file_discord_message_contributor_id_idx ON file_discord_message_relationships USING btree ("contributor_id")', 'DROP INDEX file_discord_message_contributor_id_idx'),
]
