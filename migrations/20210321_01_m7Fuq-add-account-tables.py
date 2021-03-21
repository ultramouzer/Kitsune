"""
Add account tables
"""

from yoyo import step

__depends__ = {'20210214_01_IljvB-index-posts-for-search'}

steps = [
    step(
        """
        CREATE TABLE account (
            id serial primary key,
            username varchar not null,
            password_hash varchar not null,
            UNIQUE(username)
        );
        """
    ),
    step(
        """
        CREATE TABLE account_post_favorite (
            id serial primary key,
            account_id int not null REFERENCES account(id),
            service varchar(20) not null,
            artist_id varchar(255) not null,
            post_id varchar(255) not null,
            UNIQUE(account_id, service, artist_id, post_id)
        );
        """
    ),
    step(
        """
        CREATE TABLE account_artist_favorite (
            id serial primary key,
            account_id int not null REFERENCES account(id),
            service varchar(20) not null,
            artist_id varchar(255) not null,
            UNIQUE(account_id, service, artist_id)
        );
        """
    )
]
