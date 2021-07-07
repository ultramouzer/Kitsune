"""
Add temp DM tables
"""

from yoyo import step

__depends__ = {'20210707_02_flWka-add-dm-tables'}

steps = [
    step("""
        CREATE TABLE unapproved_dms (
            "import_id" varchar(255) NOT NULL,
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
    """, "DROP TABLE unapproved_dms"),
]
