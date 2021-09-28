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
            inline boolean not null DEFAULT FALSE
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
            contributor_id varchar REFERENCES account(id)
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
        "DROP TABLE account;"
    )
]
