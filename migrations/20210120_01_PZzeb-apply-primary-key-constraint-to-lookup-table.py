"""
Apply primary key constraint to lookup table
"""

from yoyo import step

__depends__ = {'20210118_02_JxKbt-add-indexes-to-posts-table'}

steps = [
    step(
        "ALTER TABLE lookup RENAME TO old_lookup",
        "ALTER TABLE old_lookup RENAME TO lookup"
    ),
    step(
        """
        CREATE TABLE lookup (
            "id" varchar(255) NOT NULL,
            "name" varchar(255) NOT NULL,
            "service" varchar(20) NOT NULL,
            "indexed" timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
            PRIMARY KEY (id, service)
        );
        """, "DROP TABLE lookup"
    ),
    step(
        "INSERT INTO lookup SELECT * FROM old_lookup ON CONFLICT DO NOTHING",
        "INSERT INTO old_lookup SELECT * FROM lookup",
    ),
    step(
        "DROP TABLE old_lookup",
        """
        CREATE TABLE old_lookup (
            "id" varchar(255) NOT NULL,
            "name" varchar(255) NOT NULL,
            "service" varchar(20) NOT NULL,
            "indexed" timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP
        );
        """
    )
]
