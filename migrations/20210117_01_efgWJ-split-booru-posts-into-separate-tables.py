"""
Split booru_posts into separate tables
"""

from yoyo import step

__depends__ = {'initial'}

steps = [
    step("""
        CREATE TABLE patreon_posts (
            "id" varchar(255) PRIMARY KEY,
            "user" varchar(255) NOT NULL,
            "service" varchar(20) NOT NULL,
            "title" text NOT NULL DEFAULT '',
            "content" text NOT NULL DEFAULT '',
            "embed" jsonb NOT NULL DEFAULT '{}',
            "shared_file" boolean NOT NULL DEFAULT '0',
            "added" timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
            "published" timestamp,
            "edited" timestamp,
            "file" jsonb NOT NULL,
            "attachments" jsonb[] NOT NULL
        );
    """, "DROP TABLE patreon_posts"),
    step("""
        CREATE TABLE fanbox_posts (
            "id" varchar(255) PRIMARY KEY,
            "user" varchar(255) NOT NULL,
            "service" varchar(20) NOT NULL,
            "title" text NOT NULL DEFAULT '',
            "content" text NOT NULL DEFAULT '',
            "embed" jsonb NOT NULL DEFAULT '{}',
            "shared_file" boolean NOT NULL DEFAULT '0',
            "added" timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
            "published" timestamp,
            "edited" timestamp,
            "file" jsonb NOT NULL,
            "attachments" jsonb[] NOT NULL
        );
    """, "DROP TABLE fanbox_posts"),
    step("""
        CREATE TABLE gumroad_posts (
            "id" varchar(255) PRIMARY KEY,
            "user" varchar(255) NOT NULL,
            "service" varchar(20) NOT NULL,
            "title" text NOT NULL DEFAULT '',
            "content" text NOT NULL DEFAULT '',
            "embed" jsonb NOT NULL DEFAULT '{}',
            "shared_file" boolean NOT NULL DEFAULT '0',
            "added" timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
            "published" timestamp,
            "edited" timestamp,
            "file" jsonb NOT NULL,
            "attachments" jsonb[] NOT NULL
        );
    """, "DROP TABLE gumroad_posts"),
    step("""
        CREATE TABLE subscribestar_posts (
            "id" varchar(255) PRIMARY KEY,
            "user" varchar(255) NOT NULL,
            "service" varchar(20) NOT NULL,
            "title" text NOT NULL DEFAULT '',
            "content" text NOT NULL DEFAULT '',
            "embed" jsonb NOT NULL DEFAULT '{}',
            "shared_file" boolean NOT NULL DEFAULT '0',
            "added" timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
            "published" timestamp,
            "edited" timestamp,
            "file" jsonb NOT NULL,
            "attachments" jsonb[] NOT NULL
        );
    """, "DROP TABLE subscribestar_posts"),
    step("""
        CREATE TABLE dlsite_posts (
            "id" varchar(255) PRIMARY KEY,
            "user" varchar(255) NOT NULL,
            "service" varchar(20) NOT NULL,
            "title" text NOT NULL DEFAULT '',
            "content" text NOT NULL DEFAULT '',
            "embed" jsonb NOT NULL DEFAULT '{}',
            "shared_file" boolean NOT NULL DEFAULT '0',
            "added" timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
            "published" timestamp,
            "edited" timestamp,
            "file" jsonb NOT NULL,
            "attachments" jsonb[] NOT NULL
        );
    """, "DROP TABLE dlsite_posts"),
    step(
        'INSERT INTO patreon_posts SELECT * FROM booru_posts WHERE service = \'patreon\' ON CONFLICT DO NOTHING',
        'INSERT INTO booru_posts SELECT * FROM patreon_posts'
    ),
    step(
        'INSERT INTO fanbox_posts SELECT * FROM booru_posts WHERE service = \'fanbox\' ON CONFLICT DO NOTHING',
        'INSERT INTO booru_posts SELECT * FROM fanbox_posts'
    ),
    step(
        'INSERT INTO subscribestar_posts SELECT * FROM booru_posts WHERE service = \'subscribestar\' ON CONFLICT DO NOTHING',
        'INSERT INTO booru_posts SELECT * FROM subscribestar_posts'
    ),
    step(
        'INSERT INTO gumroad_posts SELECT * FROM booru_posts WHERE service = \'gumroad\' ON CONFLICT DO NOTHING',
        'INSERT INTO booru_posts SELECT * FROM gumroad_posts'
    ),
    step(
        'INSERT INTO dlsite_posts SELECT * FROM booru_posts WHERE service = \'dlsite\'',
        'INSERT INTO booru_posts SELECT * FROM dlsite_posts'
    ),
    step(
        'DROP TABLE booru_posts',
        """
        CREATE TABLE IF NOT EXISTS booru_posts (
            "id" varchar(255) NOT NULL,
            "user" varchar(255) NOT NULL,
            "service" varchar(20) NOT NULL,
            "title" text NOT NULL DEFAULT '',
            "content" text NOT NULL DEFAULT '',
            "embed" jsonb NOT NULL DEFAULT '{}',
            "shared_file" boolean NOT NULL DEFAULT '0',
            "added" timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
            "published" timestamp,
            "edited" timestamp,
            "file" jsonb NOT NULL,
            "attachments" jsonb[] NOT NULL
        );
        """
    )
]
