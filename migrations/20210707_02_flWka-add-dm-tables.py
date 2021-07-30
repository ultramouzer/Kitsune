"""
Add DM tables
"""

from yoyo import step

__depends__ = {'20210707_01_favHK-add-comment-indexes'}

steps = [
    step("""
        CREATE TABLE dms (
            "id" varchar(255) NOT NULL,
            "user" varchar(255) NOT NULL,
            "service" varchar(20) NOT NULL,
            "content" text NOT NULL DEFAULT '',
            "embed" jsonb NOT NULL DEFAULT '{}',
            "added" timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
            "published" timestamp,
            "file" jsonb NOT NULL,
            PRIMARY KEY (id, service)
        );
    """, "DROP TABLE dms"),
]
