"""
Add unique constraint to service and post fields
"""

from yoyo import step

__depends__ = {"initial"}

steps = [
    step("""
        CREATE TABLE posts (
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
            "attachments" jsonb[] NOT NULL,
            PRIMARY KEY (id, service)
        );
    """, "DROP TABLE posts"),
    step(
        "INSERT INTO posts SELECT * FROM booru_posts ON CONFLICT DO NOTHING"
        "INSERT INTO booru_posts SELECT * FROM posts"
    ),
    step(
        "DROP TABLE booru_posts",
        """
        CREATE TABLE posts (
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
